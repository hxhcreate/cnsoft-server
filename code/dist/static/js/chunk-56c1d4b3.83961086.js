(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-56c1d4b3"],{1:function(e,t){},"4b58":function(e,t,o){e.exports=o.p+"static/img/background.53576a46.jpeg"},"5cf1":function(e,t,o){},"8de4":function(e,t,o){"use strict";o.d(t,"a",(function(){return s}));var i=o("24e5"),r=o.n(i),n="MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANL378k3RiZHWx5AfJqdH9xRNBmD9wGD\n2iRe41HdTNF8RUhNnHit5NpMNtGL0NPTSSpPjjI1kJfVorRvaQerUgkCAwEAAQ==";function s(e){var t=new r.a;return t.setPublicKey(n),t.encrypt(e)}},dd7b:function(e,t,o){"use strict";o.r(t);var i=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"login",style:"background-image:url("+e.Background+");"},[o("el-form",{ref:"loginForm",staticClass:"login-form",attrs:{model:e.loginForm,rules:e.loginRules,"label-position":"left","label-width":"0px"}},[o("h3",{staticClass:"title"},[e._v("EL-ADMIN 后台管理系统")]),e._v(" "),o("el-form-item",{attrs:{prop:"username"}},[o("el-input",{attrs:{type:"text","auto-complete":"off",placeholder:"账号"},model:{value:e.loginForm.username,callback:function(t){e.$set(e.loginForm,"username",t)},expression:"loginForm.username"}},[o("svg-icon",{staticClass:"el-input__icon input-icon",attrs:{slot:"prefix","icon-class":"user"},slot:"prefix"})],1)],1),e._v(" "),o("el-form-item",{attrs:{prop:"password"}},[o("el-input",{attrs:{type:"password","auto-complete":"off",placeholder:"密码"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleLogin.apply(null,arguments)}},model:{value:e.loginForm.password,callback:function(t){e.$set(e.loginForm,"password",t)},expression:"loginForm.password"}},[o("svg-icon",{staticClass:"el-input__icon input-icon",attrs:{slot:"prefix","icon-class":"password"},slot:"prefix"})],1)],1),e._v(" "),o("el-form-item",{attrs:{prop:"code"}},[o("el-input",{staticStyle:{width:"63%"},attrs:{"auto-complete":"off",placeholder:"验证码"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleLogin.apply(null,arguments)}},model:{value:e.loginForm.code,callback:function(t){e.$set(e.loginForm,"code",t)},expression:"loginForm.code"}},[o("svg-icon",{staticClass:"el-input__icon input-icon",attrs:{slot:"prefix","icon-class":"validCode"},slot:"prefix"})],1),e._v(" "),o("div",{staticClass:"login-code"},[o("img",{attrs:{src:e.codeUrl},on:{click:e.getCode}})])],1),e._v(" "),o("el-checkbox",{staticStyle:{margin:"0 0 25px 0"},model:{value:e.loginForm.rememberMe,callback:function(t){e.$set(e.loginForm,"rememberMe",t)},expression:"loginForm.rememberMe"}},[e._v("\n      记住我\n    ")]),e._v(" "),o("el-form-item",{staticStyle:{width:"100%"}},[o("el-button",{staticStyle:{width:"100%"},attrs:{loading:e.loading,size:"medium",type:"primary"},nativeOn:{click:function(t){return t.preventDefault(),e.handleLogin.apply(null,arguments)}}},[e.loading?o("span",[e._v("登 录 中...")]):o("span",[e._v("登 录")])])],1)],1),e._v(" "),e.$store.state.settings.showFooter?o("div",{attrs:{id:"el-login-footer"}},[o("span",{domProps:{innerHTML:e._s(e.$store.state.settings.footerTxt)}}),e._v(" "),o("span",[e._v(" ⋅ ")]),e._v(" "),o("a",{attrs:{href:"https://beian.miit.gov.cn/#/Integrated/index",target:"_blank"}},[e._v(e._s(e.$store.state.settings.caseNumber))])]):e._e()],1)},r=[],n=(o("8de4"),o("83d6")),s=o.n(n),a=o("7ded"),l=o("a78e"),c=o.n(l),d=o("4328"),u=o.n(d),m=o("4b58"),p=o.n(m),g={name:"Login",data:function(){return{Background:p.a,codeUrl:"",cookiePass:"",loginForm:{username:"admin",password:"123456",rememberMe:!1,code:"",uuid:""},loginRules:{username:[{required:!0,trigger:"blur",message:"用户名不能为空"}],password:[{required:!0,trigger:"blur",message:"密码不能为空"}],code:[{required:!0,trigger:"change",message:"验证码不能为空"}]},loading:!1,redirect:void 0}},watch:{$route:{handler:function(e){var t=e.query;t&&t.redirect&&(this.redirect=t.redirect,delete t.redirect,"{}"!==JSON.stringify(t)&&(this.redirect=this.redirect+"&"+u.a.stringify(t,{indices:!1})))},immediate:!0}},created:function(){this.getCode(),this.getCookie(),this.point()},methods:{getCode:function(){var e=this;Object(a["a"])().then((function(t){e.codeUrl=t.img,e.loginForm.uuid=t.uuid}))},getCookie:function(){var e=c.a.get("username"),t=c.a.get("password"),o=c.a.get("rememberMe");this.cookiePass=void 0===t?"":t,t=void 0===t?this.loginForm.password:t,this.loginForm={username:void 0===e?this.loginForm.username:e,password:t,rememberMe:void 0!==o&&Boolean(o),code:""}},handleLogin:function(){var e=this;this.$refs.loginForm.validate((function(t){var o={username:e.loginForm.username,password:e.loginForm.password,rememberMe:e.loginForm.rememberMe,code:e.loginForm.code,uuid:e.loginForm.uuid};if(o.password,e.cookiePass,!t)return!1;e.loading=!0,o.rememberMe?(c.a.set("username",o.username,{expires:s.a.passCookieExpires}),c.a.set("password",o.password,{expires:s.a.passCookieExpires}),c.a.set("rememberMe",o.rememberMe,{expires:s.a.passCookieExpires})):(c.a.remove("username"),c.a.remove("password"),c.a.remove("rememberMe")),e.$store.dispatch("Login",o).then((function(){e.loading=!1,e.$router.push({path:e.redirect||"/"})})).catch((function(){e.loading=!1,e.getCode()}))}))},point:function(){var e=void 0!==c.a.get("point");e&&(this.$notify({title:"提示",message:"当前登录状态已过期，请重新登录！",type:"warning",duration:5e3}),c.a.remove("point"))}}},f=g,v=(o("eecc"),o("2877")),h=Object(v["a"])(f,i,r,!1,null,null,null);t["default"]=h.exports},eecc:function(e,t,o){"use strict";o("5cf1")}}]);