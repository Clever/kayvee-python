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

log = logger.Logger("logger-test")
log.info("information-log-title", dict(id=name_id, context=context_str)

# Pass global variables:
log = logger.Logger("logger-test", default_fields=dict("query"=query))
log.info("msg-title")
```

Other functions supported for structured logging:

* `Logger.debug`
* `Logger.info`
* `Logger.warn`
* `Logger.error`
* `Logger.critical`

Supported metrics:

* `Logger.counter`
* `Logger.gauge`
