# Elevator Maintenance
The problem description for this one was something about updating elevator software correctly, but it's really just
version parsing and comparing.

Parsing is fairly trivial, just watch out for things like "2.0" being different from "2.0.0". I dealt with the problem
by using `None` for empty fields, but thinking about it now I probably could have used `-1` instead which would have
saved me a little extra conversion code when comparing values. Speaking of comparison, I used the fact that Python
will compare tuples to just generate `(major, minor, patch)` tuples for each `Version` and compared them. You can
see the whole thing in the code, but the only really tricky part was adding in the `-1` values in place of `None`
in the tuples. You have to explicitly check for `is None` becuase otherwise `0` will turn into `-1` and that would
be bad. Anyways, this one took me only about 30 minutes, which was a relief after the previous problem.
