kayvee-python
=============

Kayvee is a library to write structured logs.
Its goal is to log a human-reable and machine parseable string, via a stringified JSON format.

## Installation

```
$ pip install kayvee
```

## Usage

**Writing a log**

Valid log levels: trace, info, warning, error, critical

```
> kayvee.info("an informative message")
{"msg": "an informative message","level":"info"}

> kayvee.error("an error")
{"msg":"an error","level":"error"}
```

**Passing additional key-val pairs to structured logs**

```
> kayvee.error("an error", {"title": "system-is-down"})
{"msg":"an error","title":"system-is-down","level":"error"}
```

**Adding default key-val pairs**

```
> kayvee.set_default_value("source", "my-app")

> kayvee.info("an informative message")
{"source":"my-app","msg":"an informative message","level":"info"}
```

NOTE: user passed key-val pairs will override defaults

```
> kayvee.set_default_value("source", "my-app")

> kayvee.set_default_value("foo", "bar")

> kayvee.info("an informative message")
{"source":"my-app","msg":"an informative message","level":"info","foo":"bar"}

> kayvee.info("an informative message", {"foo":"override"})
{"source":"my-app","msg":"an informative message","level":"info","foo":"override"}
```

**Emitting a metric**

Our convention is to name metrics as `<source>.<title>`.
The best practice is to set `source` (the name of the application emitting the log) as a default value.
If `source` is not set, its default value for gauges and counters is "unknown".

```
> kayvee.set_default_value("source", "my-app")

> kayvee.counter("some-event")
{"source":"my-app","title":"some-event",value":1,"type":"counter","level":"info"}

> kayvee.counter("some-event", value=5)
{"source":"my-app","title":"some-event",value":5,"type":"counter","level":"info"}

> kayvee.gauge("happiness-meter", value=11)
{"source":"my-app","title":"happiness-meter","value":11,"type":"gauge","level":"info"}
```
