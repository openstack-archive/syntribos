=========
syntribos
=========

SYNOPSIS
~~~~~~~~

syntribos [-h] [--colorize] [--config-dir DIR] [--config-file PATH]
          [--excluded-types EXCLUDED_TYPES] [--format OUTPUT_FORMAT]
          [--min-confidence MIN_CONFIDENCE]
          [--min-severity MIN_SEVERITY] [--nocolorize]
          [--outfile OUTFILE] [--test-types TEST_TYPES]
          [--syntribos-endpoint SYNTRIBOS_ENDPOINT]
          [--syntribos-exclude_results SYNTRIBOS_EXCLUDE_RESULTS]
          [--syntribos-payloads SYNTRIBOS_PAYLOADS_DIR]
          [--syntribos-templates SYNTRIBOS_TEMPLATES]
          {list_tests,run,dry_run} ...

DESCRIPTION
~~~~~~~~~~~

Syntribos is an automated API security testing tool.

Given a simple configuration file and an example HTTP request, syntribos
can replace any API URL, URL parameter, HTTP header and request body
field with a given set of strings. Syntribos aims to automatically detect
common security defects such as SQL injection, LDAP injection, buffer
overflow, etc. In addition, syntribos can be used to help identifying new
security defects by fuzzing.

Syntribos has the capability to test any API, but is designed with
OpenStack applications in mind.

OPTIONS
~~~~~~~

  -h, --help            show this help message and exit
  --colorize, -cl       Enable color in syntribos terminal output
  --config-dir DIR      Path to a config directory to pull ``*.conf`` files
                        from. This file set is sorted, so as to provide a
                        predictable parse order if individual options are
                        over-ridden. The set is parsed after the file(s)
                        specified via previous --config-file, arguments hence
                        over-ridden options in the directory take precedence.
  --config-file PATH    Path to a config file to use. Multiple config files
                        can be specified, with values in later files taking
                        precedence. Defaults to None.
  --excluded-types EXCLUDED_TYPES, -e EXCLUDED_TYPES
                        Test types to be excluded from current run against the
                        target API
  --format OUTPUT_FORMAT, -f OUTPUT_FORMAT
                        The format for outputting results
  --min-confidence MIN_CONFIDENCE, -C MIN_CONFIDENCE
                        Select a minimum confidence for reported defects
  --min-severity MIN_SEVERITY, -S MIN_SEVERITY
                        Select a minimum severity for reported defects
  --nocolorize          The inverse of --colorize
  --outfile OUTFILE, -o OUTFILE
                        File to print output to
  --test-types TEST_TYPES, -t TEST_TYPES
                        Test types to run against the target API

Main Syntribos Config:
  --syntribos-endpoint SYNTRIBOS_ENDPOINT
                        The target host to be tested
  --syntribos-exclude_results SYNTRIBOS_EXCLUDE_RESULTS
                        Defect types to exclude from the results output
  --syntribos-payloads SYNTRIBOS_PAYLOADS_DIR
                        The location where we can find syntribos' payloads
  --syntribos-templates SYNTRIBOS_TEMPLATES
                        A directory of template files, or a single template
                        file, to test on the target API

Syntribos Commands:
  {list_tests,run,dry_run}
            Available commands
    list_tests          List all available tests
    run                 Run syntribos with given config options
    dry_run             Dry run syntribos with given config options

FILES
~~~~~

~/.syntribos/syntribos.conf
  syntribos configuration file

EXAMPLES
~~~~~~~~

To run syntribos against all the available tests, just specify the
command ``syntribos run`` with the configuration file without
specifying any test type.

::

    $ syntribos --config-file keystone.conf run

SEE ALSO
~~~~~~~~

bandit(1)
