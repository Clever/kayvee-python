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
import kayvee.logger as logger

log = logger.Logger("logger-test")
log.info("information-log-title", dict(id=name_id, context=context_str))

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

## Releasing a new version

When you merge changes for a new version:

- bump the `VERSION`
- update `CHANGELOG.md` explaining the changes
- after merging, run `publish.sh`
    - requires you to install twine and wheel via `pip install <package>`
    - creates a git tag associating the version with the commit
    - publishes the versioned package to pypi (Python package store)

If you have any issues, please work with `#oncall-infra`.
