import time
import functools
import random
from typing import Any, Callable, TypeVar, cast
import structlog
from circuitbreaker import circuit
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger()

T = TypeVar('T')

def resilient_call(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """
    Executa uma função com tratamento de erros e retries
    
    Args:
        func: Função a ser executada
        *args: Argumentos posicionais para a função
        **kwargs: Argumentos nomeados para a função
        
    Returns:
        Resultado da função
    """
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                logger.error("max_retries_reached", error=str(e), retries=retry_count)
                raise
                
            # Backoff exponencial com jitter
            wait_time = (2 ** retry_count) + random.uniform(0, 1)
            logger.warning("retry_attempt", 
                          attempt=retry_count, 
                          max_retries=max_retries, 
                          wait_time=wait_time, 
                          error=str(e))
            time.sleep(wait_time)

def circuit_breaker(failure_threshold: int = 5, recovery_timeout: int = 30) -> Callable:
    """
    Decorator para implementar o padrão Circuit Breaker
    
    Args:
        failure_threshold: Número de falhas antes de abrir o circuito
        recovery_timeout: Tempo em segundos para tentar fechar o circuito
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @circuit(failure_threshold=failure_threshold, recovery_timeout=recovery_timeout)
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return func(*args, **kwargs)
        return wrapper
    return decorator

def retry_with_exponential_backoff(max_attempts: int = 3, 
                                  min_wait: float = 1, 
                                  max_wait: float = 10) -> Callable:
    """
    Decorator para retry com backoff exponencial
    
    Args:
        max_attempts: Número máximo de tentativas
        min_wait: Tempo mínimo de espera entre tentativas
        max_wait: Tempo máximo de espera entre tentativas
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
            reraise=True
        )
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return func(*args, **kwargs)
        return wrapper
    return decorator