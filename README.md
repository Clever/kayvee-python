# kayvee-python

Kayvee translates an dictionary into a human and machine parseable string, with a "json" format.

## Usage

The Kayvee formatter can be used directly or through the `kayvee.logger`

### kayvee formatter

```python
import kayvee as kv

print(kv.format(source="logger-test",
                level=kv.INFO,
                title="informational-log-title",
                dict(id=name_id, context=context_str))
```

### kayvee.logger

```python
import kayvee.logger

logger.Logger("logger-test")
logger.infoD("information-log-title", dict(id=name_id, context=context_str)
```

Other functions supported for structured logging:

* `logger.debug`
* `logger.info`
* `logger.warn`
* `logger.error`
* `logger.critical`

Supported metrics:

* `logger.counter`
* `logger.gauge`
