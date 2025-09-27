# Python API Observability Framework (TAO)

TAO is our lightweight, powerful observability framework designed specifically for Python-based APIs. It provides seamless integration of metrics, traces, and logs with minimal configuration.

## Features

- 🔄 Auto-instrumentation for FastAPI routes
- 📊 Built-in metrics collection (response times, error rates, request counts)
- 🔍 Distributed tracing with OpenTelemetry compatibility
- 📝 Structured logging with context correlation
- 🎯 Custom metric decorators
- 🔌 Pluggable backend support (Prometheus, Jaeger, ELK)

## Quick Start

```python
from tao.core import init_tao, observe
from fastapi import FastAPI

# Initialize TAO with default settings
init_tao({
    "service_name": "my-api",
    "environment": "production"
})

app = FastAPI()

# Automatically instrument all routes
app.add_middleware(observe())
```

## Decorators

TAO provides decorators for fine-grained observability:

```python
from tao.core import measure, trace, log
from typing import Dict, Any

class UserService:
    @measure('user.creation.time')
    @trace('user-creation')
    @log('debug')
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Your implementation
        pass
```

## Custom Metrics

```python
from tao.core import MetricRegistry

# Create a custom counter
request_counter = MetricRegistry.counter(
    name='api_requests_total',
    labels=['endpoint', 'status']
)

# Increment the counter
request_counter.inc({'endpoint': '/api/users', 'status': '200'})
```

## Trace Context

TAO automatically propagates trace context across service boundaries using W3C Trace Context headers:

```python
from tao.core import get_trace_context, with_context
import httpx

async def make_downstream_call():
    context = get_trace_context()
    
    async with httpx.AsyncClient() as client:
        return await client.get(
            'http://other-service/api',
            headers=with_context(context)
        )
```

## Configuration

```python
init_tao({
    "service_name": "my-api",
    "environment": "production",
    "metrics": {
        "backend": "prometheus",
        "endpoint": "/metrics"
    },
    "tracing": {
        "backend": "jaeger",
        "sampling_rate": 0.1
    },
    "logging": {
        "level": "info",
        "format": "json"
    }
})
```

## Best Practices

1. **Use Meaningful Names**: Choose descriptive names for metrics and traces
2. **Add Labels**: Include relevant labels for better filtering and aggregation
3. **Sample Wisely**: Configure appropriate sampling rates for high-traffic services
4. **Correlate Data**: Use trace IDs in logs for better debugging
5. **Monitor Resource Usage**: Enable built-in resource metrics collection