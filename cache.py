import os
import pickle
import time
import functools
from typing import Any, Callable, Optional, TypeVar, cast

T = TypeVar('T')

def _get_cache_path(prefix: str, args: tuple, kwargs: dict) -> str:
    """Gera um caminho de arquivo de cache baseado nos argumentos da função"""
    cache_dir = os.getenv("CACHE_DIR", ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    # Cria uma string representando os argumentos
    args_str = "_".join([str(arg) for arg in args])
    kwargs_str = "_".join([f"{k}_{v}" for k, v in kwargs.items()])
    
    # Combina para criar um nome de arquivo único
    filename = f"{prefix}_{args_str}_{kwargs_str}".replace("/", "_").replace(":", "_")
    if len(filename) > 200:  # Evita nomes de arquivo muito longos
        import hashlib
        filename = f"{prefix}_{hashlib.md5((args_str + kwargs_str).encode()).hexdigest()}"
    
    return os.path.join(cache_dir, filename)

def cached(prefix: str, ttl: int = 3600) -> Callable:
    """
    Decorator para cache de função com TTL
    
    Args:
        prefix: Prefixo para o arquivo de cache
        ttl: Tempo de vida do cache em segundos
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            cache_path = _get_cache_path(prefix, args, kwargs)
            
            # Verifica se o cache existe e não expirou
            if os.path.exists(cache_path):
                file_age = time.time() - os.path.getmtime(cache_path)
                if file_age < ttl:
                    try:
                        with open(cache_path, 'rb') as f:
                            return cast(T, pickle.load(f))
                    except (pickle.PickleError, EOFError):
                        # Se houver erro ao carregar o cache, ignora e recalcula
                        pass
            
            # Se não há cache válido, executa a função
            result = func(*args, **kwargs)
            
            # Salva o resultado no cache
            if result is not None:
                try:
                    with open(cache_path, 'wb') as f:
                        pickle.dump(result, f)
                except (pickle.PickleError, IOError):
                    # Se não conseguir salvar o cache, apenas ignora
                    pass
                    
            return result
        return wrapper
    return decorator

def clear_cache(prefix: Optional[str] = None) -> int:
    """
    Limpa arquivos de cache
    
    Args:
        prefix: Se fornecido, limpa apenas os arquivos com este prefixo
        
    Returns:
        Número de arquivos removidos
    """
    cache_dir = os.getenv("CACHE_DIR", ".cache")
    if not os.path.exists(cache_dir):
        return 0
        
    count = 0
    for filename in os.listdir(cache_dir):
        if prefix is None or filename.startswith(prefix):
            try:
                os.remove(os.path.join(cache_dir, filename))
                count += 1
            except OSError:
                pass
                
    return count