# cloud_onprem

If you want to test on vmkiwi-test include following in your code:

```import sys

sys.path.insert(0, '/secbin/security/cms_wrapper/lib')

from cms_wrapper import CMSWrapper
```

under name=='main':

```
a=CMSWrapper() a.allow_cloudweb = False
```
