TODO
~~~~

global
------
- What use is the no_redirect in the urls ?


base.html
---------
- Don't hardcode the bugzilla version
- Create a real "My Bugs" link
- Don't hardcode href in the head


home.html
---------
- docs/en/html/using.html


new_bug.html
------------
- don't hardcode the product for view-component url
- Remove hardcoded TestProduct


bug_list
--------
- Create the zarro bug template
- Hardcoded list filters
- default resolution should be "---" instead of ""


create_account.html
-------------------
- remove hardcoded bugzilla admin email
- make a real account creation form


index
-----
- logout: index.cgi?logout=1
- forgot password: index.cgi?GoAheadAndLogIn=1#forgot


view-component
--------------
- describecomponents.cgi?product=TestProduct


create_account
--------------
- write the form


history template tags
---------------------
- create_filtered_query_string: add the extra arguments
