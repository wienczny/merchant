Making merchant, the library that talks to multiple payment gateways and
processors framework agnostic.

Highly alpha and lots of components still require work. Hopefully, this
will go upstream when the work is complete.

Initial plans to support:

* django
* flask


----------------
Support Matrix
----------------

+--------------------------+----------+----------+
|                          |  Django  |  Flask   |
+--------------------------+----------+----------+
| Stripe                   |    Y     |    Y     |
+--------------------------+----------+----------+

Other framework support may be community contributed.

Things to do
--------------

* Make the merchant (base) library framework agnostic ie it will not contain
  any forms, urlpatterns etc and will act as a base for the frameworks
* Write separate documentation for each framework
* Improve the examples for each framework
* Upload each of the packages to pypi
* Add more items when I recollect them...

