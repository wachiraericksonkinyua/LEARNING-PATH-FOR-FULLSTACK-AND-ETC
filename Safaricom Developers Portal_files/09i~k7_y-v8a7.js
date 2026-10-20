(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,47025,(e,t,r)=>{"use strict";var a=e.r(78509);Object.defineProperty(r,"__esModule",{value:!0}),r.default=void 0;var i=a(e.r(21506)),s=e.r(91398);r.default=(0,i.default)((0,s.jsx)("path",{d:"M21 11H6.83l3.58-3.59L9 6l-6 6 6 6 1.41-1.41L6.83 13H21z"}),"KeyboardBackspaceOutlined")},27773,(e,t,r)=>{"use strict";var a=e.r(78509);Object.defineProperty(r,"__esModule",{value:!0}),r.default=void 0;var i=a(e.r(21506)),s=e.r(91398);r.default=(0,i.default)((0,s.jsx)("path",{d:"m15 5-1.41 1.41L18.17 11H2v2h16.17l-4.59 4.59L15 19l7-7z"}),"East")},32854,e=>{"use strict";e.i(68681);var t=e.i(5578),r=e.i(91788),a=e.i(23289),i=!1,s=r.useSyncExternalStore||function(e,s,n){var l=s();!1===globalThis.__DEV__||i||l===s()||(i=!0,!1!==globalThis.__DEV__&&t.invariant.error(56));var u=r.useState({inst:{value:l,getSnapshot:s}}),d=u[0].inst,c=u[1];return a.canUseLayoutEffect?r.useLayoutEffect(function(){Object.assign(d,{value:l,getSnapshot:s}),o(d)&&c({inst:d})},[e,l,s]):Object.assign(d,{value:l,getSnapshot:s}),r.useEffect(function(){return o(d)&&c({inst:d}),e(function(){o(d)&&c({inst:d})})},[e]),l};function o(e){var t=e.value,r=e.getSnapshot;try{return t!==r()}catch(e){return!0}}e.s(["useSyncExternalStore",0,s])},32171,76810,e=>{"use strict";var t,r,a=e.i(89280);e.i(68681);var i=e.i(5578),s=e.i(91788),o=e.i(32854),n=e.i(24669),l=e.i(69570),u=e.i(21805),d=e.i(33879);(t=r||(r={}))[t.loading=1]="loading",t[t.setVariables=2]="setVariables",t[t.fetchMore=3]="fetchMore",t[t.refetch=4]="refetch",t[t.poll=6]="poll",t[t.ready=7]="ready",t[t.error=8]="error",e.s(["NetworkStatus",0,r,"isNetworkRequestInFlight",0,function(e){return!!e&&e<7}],76810);var c=e.i(60601),p=e.i(98926),h=e.i(23289),f=e.i(27371),g=e.i(42419),m=e.i(11922),y=Object.prototype.hasOwnProperty;function b(e,t){var r=s.useRef();r.current&&e===r.current.client&&t===r.current.query||(r.current=new v(e,t,r.current));var a=r.current;return a.forceUpdateState=s.useReducer(function(e){return e+1},0)[1],a}var v=function(){function e(e,t,a){var i=this;this.client=e,this.query=t,this.forceUpdate=function(){return i.forceUpdateState()},this.ssrDisabledResult=(0,m.maybeDeepFreeze)({loading:!0,data:void 0,error:void 0,networkStatus:r.loading}),this.skipStandbyResult=(0,m.maybeDeepFreeze)({loading:!1,data:void 0,error:void 0,networkStatus:r.ready}),this.toQueryResultCache=new(h.canUseWeakMap?WeakMap:Map),(0,c.verifyDocumentType)(t,c.DocumentType.Query);var s=a&&a.result,o=s&&s.data;o&&(this.previousData=o)}return e.prototype.forceUpdateState=function(){!1!==globalThis.__DEV__&&i.invariant.warn(48)},e.prototype.executeQuery=function(e){var t,r=this;e.query&&Object.assign(this,{query:e.query}),this.watchQueryOptions=this.createWatchQueryOptions(this.queryHookOptions=e);var a=this.observable.reobserveAsConcast(this.getObsQueryOptions());return this.previousData=(null==(t=this.result)?void 0:t.data)||this.previousData,this.result=void 0,this.forceUpdate(),new Promise(function(e){var t;a.subscribe({next:function(e){t=e},error:function(){e(r.toQueryResult(r.observable.getCurrentResult()))},complete:function(){e(r.toQueryResult(t))}})})},e.prototype.useQuery=function(e){var t=this;this.renderPromises=s.useContext((0,u.getApolloContext)()).renderPromises,this.useOptions(e);var a=this.useObservableQuery(),i=(0,o.useSyncExternalStore)(s.useCallback(function(e){if(t.renderPromises)return function(){};t.forceUpdate=e;var i=function(){var e=t.result,r=a.getCurrentResult();e&&e.loading===r.loading&&e.networkStatus===r.networkStatus&&(0,n.equal)(e.data,r.data)||t.setResult(r)},s=function(e){if(o.unsubscribe(),o=a.resubscribeAfterError(i,s),!y.call(e,"graphQLErrors"))throw e;var l=t.result;(!l||l&&l.loading||!(0,n.equal)(e,l.error))&&t.setResult({data:l&&l.data,error:e,loading:!1,networkStatus:r.error})},o=a.subscribe(i,s);return function(){setTimeout(function(){return o.unsubscribe()}),t.forceUpdate=function(){return t.forceUpdateState()}}},[a,this.renderPromises,this.client.disableNetworkFetches]),function(){return t.getCurrentResult()},function(){return t.getCurrentResult()});return this.unsafeHandlePartialRefetch(i),this.toQueryResult(i)},e.prototype.useOptions=function(t){var r,a=this.createWatchQueryOptions(this.queryHookOptions=t),i=this.watchQueryOptions;!(0,n.equal)(a,i)&&(this.watchQueryOptions=a,i&&this.observable&&(this.observable.reobserve(this.getObsQueryOptions()),this.previousData=(null==(r=this.result)?void 0:r.data)||this.previousData,this.result=void 0)),this.onCompleted=t.onCompleted||e.prototype.onCompleted,this.onError=t.onError||e.prototype.onError,(this.renderPromises||this.client.disableNetworkFetches)&&!1===this.queryHookOptions.ssr&&!this.queryHookOptions.skip?this.result=this.ssrDisabledResult:this.queryHookOptions.skip||"standby"===this.watchQueryOptions.fetchPolicy?this.result=this.skipStandbyResult:(this.result===this.ssrDisabledResult||this.result===this.skipStandbyResult)&&(this.result=void 0)},e.prototype.getObsQueryOptions=function(){var e=[],t=this.client.defaultOptions.watchQuery;return t&&e.push(t),this.queryHookOptions.defaultOptions&&e.push(this.queryHookOptions.defaultOptions),e.push((0,f.compact)(this.observable&&this.observable.options,this.watchQueryOptions)),e.reduce(l.mergeOptions)},e.prototype.createWatchQueryOptions=function(e){void 0===e&&(e={});var t,r=e.skip,i=Object.assign((e.ssr,e.onCompleted,e.onError,e.defaultOptions,(0,a.__rest)(e,["skip","ssr","onCompleted","onError","defaultOptions"])),{query:this.query});if(this.renderPromises&&("network-only"===i.fetchPolicy||"cache-and-network"===i.fetchPolicy)&&(i.fetchPolicy="cache-first"),i.variables||(i.variables={}),r){var s=i.fetchPolicy,o=void 0===s?this.getDefaultFetchPolicy():s,n=i.initialFetchPolicy;Object.assign(i,{initialFetchPolicy:void 0===n?o:n,fetchPolicy:"standby"})}else i.fetchPolicy||(i.fetchPolicy=(null==(t=this.observable)?void 0:t.options.initialFetchPolicy)||this.getDefaultFetchPolicy());return i},e.prototype.getDefaultFetchPolicy=function(){var e,t;return(null==(e=this.queryHookOptions.defaultOptions)?void 0:e.fetchPolicy)||(null==(t=this.client.defaultOptions.watchQuery)?void 0:t.fetchPolicy)||"cache-first"},e.prototype.onCompleted=function(e){},e.prototype.onError=function(e){},e.prototype.useObservableQuery=function(){var e=this.observable=this.renderPromises&&this.renderPromises.getSSRObservable(this.watchQueryOptions)||this.observable||this.client.watchQuery(this.getObsQueryOptions());this.obsQueryFields=s.useMemo(function(){return{refetch:e.refetch.bind(e),reobserve:e.reobserve.bind(e),fetchMore:e.fetchMore.bind(e),updateQuery:e.updateQuery.bind(e),startPolling:e.startPolling.bind(e),stopPolling:e.stopPolling.bind(e),subscribeToMore:e.subscribeToMore.bind(e)}},[e]);var t=!(!1===this.queryHookOptions.ssr||this.queryHookOptions.skip);return this.renderPromises&&t&&(this.renderPromises.registerSSRObservable(e),e.getCurrentResult().loading&&this.renderPromises.addObservableQueryPromise(e)),e},e.prototype.setResult=function(e){var t=this.result;t&&t.data&&(this.previousData=t.data),this.result=e,this.forceUpdate(),this.handleErrorOrCompleted(e,t)},e.prototype.handleErrorOrCompleted=function(e,t){var a=this;if(!e.loading){var s=this.toApolloError(e);Promise.resolve().then(function(){s?a.onError(s):e.data&&(null==t?void 0:t.networkStatus)!==e.networkStatus&&e.networkStatus===r.ready&&a.onCompleted(e.data)}).catch(function(e){!1!==globalThis.__DEV__&&i.invariant.warn(e)})}},e.prototype.toApolloError=function(e){return(0,g.isNonEmptyArray)(e.errors)?new d.ApolloError({graphQLErrors:e.errors}):e.error},e.prototype.getCurrentResult=function(){return this.result||this.handleErrorOrCompleted(this.result=this.observable.getCurrentResult()),this.result},e.prototype.toQueryResult=function(e){var t=this.toQueryResultCache.get(e);if(t)return t;var r=e.data,i=(e.partial,(0,a.__rest)(e,["data","partial"]));return this.toQueryResultCache.set(e,t=(0,a.__assign)((0,a.__assign)((0,a.__assign)({data:r},i),this.obsQueryFields),{client:this.client,observable:this.observable,variables:this.observable.variables,called:!this.queryHookOptions.skip,previousData:this.previousData})),!t.error&&(0,g.isNonEmptyArray)(e.errors)&&(t.error=new d.ApolloError({graphQLErrors:e.errors})),t},e.prototype.unsafeHandlePartialRefetch=function(e){e.partial&&this.queryHookOptions.partialRefetch&&!e.loading&&(!e.data||0===Object.keys(e.data).length)&&"cache-only"!==this.observable.options.fetchPolicy&&(Object.assign(e,{loading:!0,networkStatus:r.refetch}),this.observable.refetch())},e}();e.s(["useInternalState",0,b,"useQuery",0,function(e,t){return void 0===t&&(t=Object.create(null)),b((0,p.useApolloClient)(t.client),e).useQuery(t)}],32171)},74872,40790,e=>{"use strict";e.i(50461);var t=e.i(91788),r=e.i(56206),a=e.i(76989),i=e.i(73086),s=e.i(81888),o=e.i(96851),n=e.i(95724),l=e.i(20466);let u=t.createContext();var d=e.i(27785),c=e.i(3466);function p(e){return(0,c.default)("MuiGrid",e)}let h=["auto",!0,1,2,3,4,5,6,7,8,9,10,11,12],f=(0,d.default)("MuiGrid",["root","container","item","zeroMinWidth",...[0,1,2,3,4,5,6,7,8,9,10].map(e=>`spacing-xs-${e}`),...["column-reverse","column","row-reverse","row"].map(e=>`direction-xs-${e}`),...["nowrap","wrap-reverse","wrap"].map(e=>`wrap-xs-${e}`),...h.map(e=>`grid-xs-${e}`),...h.map(e=>`grid-sm-${e}`),...h.map(e=>`grid-md-${e}`),...h.map(e=>`grid-lg-${e}`),...h.map(e=>`grid-xl-${e}`)]);var g=e.i(91398);function m({breakpoints:e,values:t}){let r="";Object.keys(t).forEach(e=>{""===r&&0!==t[e]&&(r=e)});let a=Object.keys(e).sort((t,r)=>e[t]-e[r]);return a.slice(0,a.indexOf(r))}let y=(0,o.default)("div",{name:"MuiGrid",slot:"Root",overridesResolver:(e,t)=>{let{ownerState:r}=e,{container:a,direction:i,item:s,spacing:o,wrap:n,zeroMinWidth:l,breakpoints:u}=r,d=[];a&&(d=function(e,t,r={}){if(!e||e<=0)return[];if("string"==typeof e&&!Number.isNaN(Number(e))||"number"==typeof e)return[r[`spacing-xs-${String(e)}`]];let a=[];return t.forEach(t=>{let i=e[t];Number(i)>0&&a.push(r[`spacing-${t}-${String(i)}`])}),a}(o,u,t));let c=[];return u.forEach(e=>{let a=r[e];a&&c.push(t[`grid-${e}-${String(a)}`])}),[t.root,a&&t.container,s&&t.item,l&&t.zeroMinWidth,...d,"row"!==i&&t[`direction-xs-${String(i)}`],"wrap"!==n&&t[`wrap-xs-${String(n)}`],...c]}})(({ownerState:e})=>({boxSizing:"border-box",...e.container&&{display:"flex",flexWrap:"wrap",width:"100%"},...e.item&&{margin:0},...e.zeroMinWidth&&{minWidth:0},..."wrap"!==e.wrap&&{flexWrap:e.wrap}}),function({theme:e,ownerState:t}){let r=(0,a.resolveBreakpointValues)({values:t.direction,breakpoints:e.breakpoints.values});return(0,a.handleBreakpoints)({theme:e},r,e=>{let t={flexDirection:e};return e.startsWith("column")&&(t[`& > .${f.item}`]={maxWidth:"none"}),t})},function({theme:e,ownerState:t}){let{container:r,rowSpacing:i}=t,s={};if(r&&0!==i){let t,r=(0,a.resolveBreakpointValues)({values:i,breakpoints:e.breakpoints.values});"object"==typeof r&&(t=m({breakpoints:e.breakpoints.values,values:r})),s=(0,a.handleBreakpoints)({theme:e},r,(r,a)=>{let i=e.spacing(r);return"0px"!==i?{marginTop:`calc(-1 * ${i})`,[`& > .${f.item}`]:{paddingTop:i}}:t?.includes(a)?{}:{marginTop:0,[`& > .${f.item}`]:{paddingTop:0}}})}return s},function({theme:e,ownerState:t}){let{container:r,columnSpacing:i}=t,s={};if(r&&0!==i){let t,r=(0,a.resolveBreakpointValues)({values:i,breakpoints:e.breakpoints.values});"object"==typeof r&&(t=m({breakpoints:e.breakpoints.values,values:r})),s=(0,a.handleBreakpoints)({theme:e},r,(r,a)=>{let i=e.spacing(r);if("0px"!==i){let e=`calc(-1 * ${i})`;return{width:`calc(100% + ${i})`,marginLeft:e,[`& > .${f.item}`]:{paddingLeft:i}}}return t?.includes(a)?{}:{width:"100%",marginLeft:0,[`& > .${f.item}`]:{paddingLeft:0}}})}return s},function({theme:e,ownerState:t}){let r;return e.breakpoints.keys.reduce((i,s)=>{let o={};if(t[s]&&(r=t[s]),!r)return i;if(!0===r)o={flexBasis:0,flexGrow:1,maxWidth:"100%"};else if("auto"===r)o={flexBasis:"auto",flexGrow:0,flexShrink:0,maxWidth:"none",width:"auto"};else{let n=(0,a.resolveBreakpointValues)({values:t.columns,breakpoints:e.breakpoints.values}),l="object"==typeof n?n[s]:n;if(null==l)return i;let u=`${Math.round(r/l*1e8)/1e6}%`,d={};if(t.container&&t.item&&0!==t.columnSpacing){let r=e.spacing(t.columnSpacing);if("0px"!==r){let e=`calc(${u} + ${r})`;d={flexBasis:e,maxWidth:e}}}o={flexBasis:u,flexGrow:0,maxWidth:u,...d}}return 0===e.breakpoints.values[s]?Object.assign(i,o):i[e.breakpoints.up(s)]=o,i},{})}),b=t.forwardRef(function(e,a){let o=(0,n.useDefaultProps)({props:e,name:"MuiGrid"}),{breakpoints:d}=(0,l.default)(),c=(0,i.extendSxProp)(o),{className:h,columns:f,columnSpacing:m,component:b="div",container:v=!1,direction:x="row",item:C=!1,rowSpacing:w,spacing:k=0,wrap:S="wrap",zeroMinWidth:O=!1,...P}=c,R=t.useContext(u),M=v?f||12:R,E={},A={...P};d.keys.forEach(e=>{null!=P[e]&&(E[e]=P[e],delete A[e])});let _={...c,columns:M,container:v,direction:x,item:C,rowSpacing:w||k,columnSpacing:m||k,wrap:S,zeroMinWidth:O,spacing:k,...E,breakpoints:d.keys},N=(e=>{let{classes:t,container:r,direction:a,item:i,spacing:o,wrap:n,zeroMinWidth:l,breakpoints:u}=e,d=[];r&&(d=function(e,t){if(!e||e<=0)return[];if("string"==typeof e&&!Number.isNaN(Number(e))||"number"==typeof e)return[`spacing-xs-${String(e)}`];let r=[];return t.forEach(t=>{let a=e[t];if(Number(a)>0){let e=`spacing-${t}-${String(a)}`;r.push(e)}}),r}(o,u));let c=[];u.forEach(t=>{let r=e[t];r&&c.push(`grid-${t}-${String(r)}`)});let h={root:["root",r&&"container",i&&"item",l&&"zeroMinWidth",...d,"row"!==a&&`direction-xs-${String(a)}`,"wrap"!==n&&`wrap-xs-${String(n)}`,...c]};return(0,s.default)(h,p,t)})(_);return(0,g.jsx)(u.Provider,{value:M,children:(0,g.jsx)(y,{ownerState:_,className:(0,r.default)(N.root,h),as:b,ref:a,...A})})});e.s(["default",0,b],40790),e.s(["Grid",0,b],74872)},37157,e=>{"use strict";var t=e.i(43906);e.s(["typographyClasses",()=>t.default])},20788,e=>{"use strict";e.i(50461);var t=e.i(91788),r=e.i(81888),a=e.i(15871),i=e.i(37157),s=e.i(80445),o=e.i(95724),n=e.i(27785),l=e.i(3466);function u(e){return(0,l.default)("MuiCardHeader",e)}let d=(0,n.default)("MuiCardHeader",["root","avatar","action","content","title","subheader"]);var c=e.i(69998),p=e.i(91398);let h=(0,s.styled)("div",{name:"MuiCardHeader",slot:"Root",overridesResolver:(e,t)=>[{[`& .${d.title}`]:t.title},{[`& .${d.subheader}`]:t.subheader},t.root]})({display:"flex",alignItems:"center",padding:16}),f=(0,s.styled)("div",{name:"MuiCardHeader",slot:"Avatar",overridesResolver:(e,t)=>t.avatar})({display:"flex",flex:"0 0 auto",marginRight:16}),g=(0,s.styled)("div",{name:"MuiCardHeader",slot:"Action",overridesResolver:(e,t)=>t.action})({flex:"0 0 auto",alignSelf:"flex-start",marginTop:-4,marginRight:-8,marginBottom:-4}),m=(0,s.styled)("div",{name:"MuiCardHeader",slot:"Content",overridesResolver:(e,t)=>t.content})({flex:"1 1 auto",[`.${i.typographyClasses.root}:where(& .${d.title})`]:{display:"block"},[`.${i.typographyClasses.root}:where(& .${d.subheader})`]:{display:"block"}}),y=t.forwardRef(function(e,t){let i=(0,o.useDefaultProps)({props:e,name:"MuiCardHeader"}),{action:s,avatar:n,component:l="div",disableTypography:d=!1,subheader:y,subheaderTypographyProps:b,title:v,titleTypographyProps:x,slots:C={},slotProps:w={},...k}=i,S={...i,component:l,disableTypography:d},O=(e=>{let{classes:t}=e;return(0,r.default)({root:["root"],avatar:["avatar"],action:["action"],content:["content"],title:["title"],subheader:["subheader"]},u,t)})(S),P={slots:C,slotProps:{title:x,subheader:b,...w}},R=v,[M,E]=(0,c.default)("title",{className:O.title,elementType:a.default,externalForwardedProps:P,ownerState:S,additionalProps:{variant:n?"body2":"h5",component:"span"}});null==R||R.type===a.default||d||(R=(0,p.jsx)(M,{...E,children:R}));let A=y,[_,N]=(0,c.default)("subheader",{className:O.subheader,elementType:a.default,externalForwardedProps:P,ownerState:S,additionalProps:{variant:n?"body2":"body1",color:"textSecondary",component:"span"}});null==A||A.type===a.default||d||(A=(0,p.jsx)(_,{...N,children:A}));let[$,j]=(0,c.default)("root",{ref:t,className:O.root,elementType:h,externalForwardedProps:{...P,...k,component:l},ownerState:S}),[T,Q]=(0,c.default)("avatar",{className:O.avatar,elementType:f,externalForwardedProps:P,ownerState:S}),[D,q]=(0,c.default)("content",{className:O.content,elementType:m,externalForwardedProps:P,ownerState:S}),[B,H]=(0,c.default)("action",{className:O.action,elementType:g,externalForwardedProps:P,ownerState:S});return(0,p.jsxs)($,{...j,children:[n&&(0,p.jsx)(T,{...Q,children:n}),(0,p.jsxs)(D,{...q,children:[R,A]}),s&&(0,p.jsx)(B,{...H,children:s})]})});e.s(["CardHeader",0,y],20788)},54393,75230,e=>{"use strict";var t=e.i(91398),r=e.i(91788),a=e.i(32171),i=e.i(91567),s=e.i(51691),o=e.i(59080);let n=o.gql`
  query GetAPIs {
    getApis {
      body {
        alias
        category
        color
        endpoint
        id
        name
        operation
        parent
        purpose
        subsidiaries
        subsidiary
      }
      message
      status
    }
  }
`,l=o.gql`
  query GetAPICategories {
    getApiCategories {
      body {
        name
        id
        color
      }
      message
      status
    }
  }
`,u=o.gql`
  query GetApiDocumentation($apiName: String!) {
    populateApi(apiName: $apiName) {
      status
      message
      body {
        apiDetails {
          alias
          category
          id
          name
          subsidiaries
          subsidiary
          parent
          color
          operation
          endpoint
          purpose
        }
        dataset {
          operation
          icon
          color
          headers
          mapping
        }
        details {
          name
          operation
          endpoint
          purpose
          alias
          parent
        }
        documentation {
          id
          priority
          parentTitle
          parentContent
          childTitle
          childContent
          grandChildTitle
          grandChildContent
          postmanCollectionLink
          addedBy
          addedOn
          modifiedBy
          modifiedOn
          apiName
        }
      }
      hasMarkdown
      markdown
      sections
    }
  }
`,d=o.gql`
  query getApiDocsMetadata {
    getApiCategories {
      status
      message
      body {
        id
        name
        color
      }
    }
    getApis {
      status
      message
      body {
        id
        name
        alias
        subsidiaries
        subsidiary
        parent
        color
        operation
        endpoint
        purpose
        category
      }
    }
  }
`,c=o.gql`
  query GetMobileCenterOnboardingForm {
    getMobileCenterOnboardingForm {
      status
      message
      body {
        id
        appName
        appUrl
        activeSubscribers
        appDownloads
        dailyUsers
        companyName
        department
        contactPersonName
        email
        phoneNumber
        displayStatus
        currentStatus
        isRejected
      }
    }
  }
`;e.s(["GET_API_CATEGORIES",0,l,"GET_API_METADATA",0,d,"GET_APIs",0,n,"GET_DOCUMENTATION",0,u,"GET_MOBILE_CENTER_ONBOARDING_FORM",0,c],75230);let p="mobile_center_app",h=(0,r.createContext)({loading:!1,apis:[],categories:[],refetchApis:()=>{},refetchApiCategories:()=>{},refetchMobileCenterData:async()=>{},mobileCenterData:null,mobileCenterLoading:!1});function f({children:e}){let{notifyError:i}=(0,s.default)(),[o,u]=(0,r.useState)([]),[d,g]=(0,r.useState)([]),[m,y]=(0,r.useState)(!1),[b,v]=(0,r.useState)(null),{data:x,loading:C,error:w,refetch:k}=(0,a.useQuery)(n),{data:S,error:O,refetch:P}=(0,a.useQuery)(l),{data:R,error:M,loading:E,refetch:A}=(0,a.useQuery)(c,{fetchPolicy:"cache-and-network",nextFetchPolicy:"cache-and-network"});(0,r.useEffect)(()=>{w&&i({message:w.message}),O&&i({message:O.message}),M&&i({message:M.message})},[w,O,M]),(0,r.useEffect)(()=>{x?.getApis?.status===!1&&i({message:x.getApis.message}),S?.getApiCategories?.status===!1&&i({message:S.getApiCategories.message})},[x,S]);let _=e=>{if(e?.isRejected!==!0)return;let t=((e="")=>{let t=String(e).trim().toLowerCase().replace(/[^a-z0-9]+/g,"_").replace(/^_+|_+$/g,"");return t?`${p}_${t}`:p})(e.appName||""),r={appDetails:{appName:e.appName||"",url:e.appUrl||"",subscribers:String(e.activeSubscribers??""),downloads:String(e.appDownloads??""),users:String(e.dailyUsers??"")},contactInfo:{companyName:e.companyName||"",department:e.department||"",contactPerson:e.contactPersonName||"",teamPhone:e.phoneNumber||"",teamEmail:e.email||"",teamPhoneVerified:!1,teamEmailVerified:!1,teamPhoneVerifiedValue:"",teamEmailVerifiedValue:"",validatedContacts:[]}};localStorage.setItem("mobile_center_app_active_key",t),localStorage.setItem(t,JSON.stringify(r))};(0,r.useEffect)(()=>{if(x?.getApis?.status&&Array.isArray(x.getApis.body)&&u(x.getApis.body.map(e=>({...e,show:!(e.subsidiary&&null!==e.Parent)}))),S?.getApiCategories?.status&&Array.isArray(S.getApiCategories.body)&&g(S.getApiCategories.body),R?.getMobileCenterOnboardingForm?.status){let e=R.getMobileCenterOnboardingForm.body;v(e),_(e)}},[x,S,R]);let N=async()=>{y(!0);try{let{data:e}=await k();e?.getApis?.status===!1&&i({message:e.getApis.message})}catch(e){i({message:e.message})}finally{setTimeout(()=>y(!1),0)}},$=async()=>{y(!0);try{let{data:e}=await P();e?.getApiCategories?.status===!1&&i({message:e.getApiCategories.message})}catch(e){i({message:e.message})}finally{setTimeout(()=>y(!1),0)}},j=(0,r.useCallback)(async()=>{try{if(!A)return!1;let e=await A({fetchPolicy:"network-only"});if(e?.data?.getMobileCenterOnboardingForm?.status){let t=e.data.getMobileCenterOnboardingForm.body;return v(t),_(t),!0}return e?.data?.getMobileCenterOnboardingForm?.status===!1&&i({message:e.data.getMobileCenterOnboardingForm.message}),!1}catch(e){return i({message:e.message}),!1}},[A,i]),T=C||m,Q=(0,r.useMemo)(()=>({loading:T,apis:o,refetchApis:N,categories:d,refetchApiCategories:$,refetchMobileCenterData:j,mobileCenterData:b,mobileCenterLoading:E}),[T,o,d,b,E,j]);return(0,t.jsx)(h.Provider,{value:Q,children:e})}f.propTypes={children:i.default.node.isRequired},e.s(["default",0,f,"useApisContext",0,()=>(0,r.useContext)(h)],54393)},6850,e=>{"use strict";e.i(50461);var t=e.i(91788),r=e.i(56206),a=e.i(81888),i=e.i(80445),s=e.i(95724),o=e.i(27785),n=e.i(3466);function l(e){return(0,n.default)("MuiCardContent",e)}(0,o.default)("MuiCardContent",["root"]);var u=e.i(91398);let d=(0,i.styled)("div",{name:"MuiCardContent",slot:"Root",overridesResolver:(e,t)=>t.root})({padding:16,"&:last-child":{paddingBottom:24}}),c=t.forwardRef(function(e,t){let i=(0,s.useDefaultProps)({props:e,name:"MuiCardContent"}),{className:o,component:n="div",...c}=i,p={...i,component:n},h=(e=>{let{classes:t}=e;return(0,a.default)({root:["root"]},l,t)})(p);return(0,u.jsx)(d,{as:n,className:(0,r.default)(h.root,o),ownerState:p,ref:t,...c})});e.s(["default",0,c],6850)},75765,e=>{"use strict";e.i(50461);var t=e.i(91788),r=e.i(56206),a=e.i(81888),i=e.i(62170),s=e.i(80445),o=e.i(95724),n=e.i(15871),l=e.i(37742),u=e.i(90117),d=e.i(59540),c=e.i(91398);let p=(0,d.default)((0,c.jsx)("path",{d:"M6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"}),"MoreHoriz");var h=e.i(41661);let f=(0,s.styled)(h.default)((0,u.default)(({theme:e})=>({display:"flex",marginLeft:`calc(${e.spacing(1)} * 0.5)`,marginRight:`calc(${e.spacing(1)} * 0.5)`,..."light"===e.palette.mode?{backgroundColor:e.palette.grey[100],color:e.palette.grey[700]}:{backgroundColor:e.palette.grey[700],color:e.palette.grey[100]},borderRadius:2,"&:hover, &:focus":{..."light"===e.palette.mode?{backgroundColor:e.palette.grey[200]}:{backgroundColor:e.palette.grey[600]}},"&:active":{boxShadow:e.shadows[0],..."light"===e.palette.mode?{backgroundColor:(0,l.emphasize)(e.palette.grey[200],.12)}:{backgroundColor:(0,l.emphasize)(e.palette.grey[600],.12)}}}))),g=(0,s.styled)(p)({width:24,height:16}),m=function(e){let{slots:t={},slotProps:r={},...a}=e;return(0,c.jsx)("li",{children:(0,c.jsx)(f,{focusRipple:!0,...a,ownerState:e,children:(0,c.jsx)(g,{as:t.CollapsedIcon,ownerState:e,...r.collapsedIcon})})})};var y=e.i(27785),b=e.i(3466);function v(e){return(0,b.default)("MuiBreadcrumbs",e)}let x=(0,y.default)("MuiBreadcrumbs",["root","ol","li","separator"]),C=(0,s.styled)(n.default,{name:"MuiBreadcrumbs",slot:"Root",overridesResolver:(e,t)=>[{[`& .${x.li}`]:t.li},t.root]})({}),w=(0,s.styled)("ol",{name:"MuiBreadcrumbs",slot:"Ol",overridesResolver:(e,t)=>t.ol})({display:"flex",flexWrap:"wrap",alignItems:"center",padding:0,margin:0,listStyle:"none"}),k=(0,s.styled)("li",{name:"MuiBreadcrumbs",slot:"Separator",overridesResolver:(e,t)=>t.separator})({display:"flex",userSelect:"none",marginLeft:8,marginRight:8}),S=t.forwardRef(function(e,s){var n,l;let u=(0,o.useDefaultProps)({props:e,name:"MuiBreadcrumbs"}),{children:d,className:p,component:h="nav",slots:f={},slotProps:g={},expandText:y="Show path",itemsAfterCollapse:b=1,itemsBeforeCollapse:x=1,maxItems:S=8,separator:O="/",...P}=u,[R,M]=t.useState(!1),E={...u,component:h,expanded:R,expandText:y,itemsAfterCollapse:b,itemsBeforeCollapse:x,maxItems:S,separator:O},A=(e=>{let{classes:t}=e;return(0,a.default)({root:["root"],li:["li"],ol:["ol"],separator:["separator"]},v,t)})(E),_=(0,i.default)({elementType:f.CollapsedIcon,externalSlotProps:g.collapsedIcon,ownerState:E}),N=t.useRef(null),$=t.Children.toArray(d).filter(e=>t.isValidElement(e)).map((e,t)=>(0,c.jsx)("li",{className:A.li,children:e},`child-${t}`));return(0,c.jsx)(C,{ref:s,component:h,color:"textSecondary",className:(0,r.default)(A.root,p),ownerState:E,...P,children:(0,c.jsx)(w,{className:A.ol,ref:N,ownerState:E,children:(n=R||S&&$.length<=S||x+b>=$.length?$:[...$.slice(0,x),(0,c.jsx)(m,{"aria-label":y,slots:{CollapsedIcon:f.CollapsedIcon},slotProps:{collapsedIcon:_},onClick:()=>{M(!0);let e=N.current.querySelector("a[href],button,[tabindex]");e&&e.focus()}},"ellipsis"),...$.slice($.length-b,$.length)],l=A.separator,n.reduce((e,t,r)=>(r<n.length-1?e=e.concat(t,(0,c.jsx)(k,{"aria-hidden":!0,className:l,ownerState:E,children:O},`separator-${r}`)):e.push(t),e),[]))})})});e.s(["Breadcrumbs",0,S],75765)},85474,e=>{"use strict";var t=e.i(91398),r=e.i(47025),a=e.i(75765);e.i(91788);var i=e.i(91567),s=e.i(3828);function o({sx:e,current:i,prevPaths:n}){let l=(0,s.useRouter)();return(0,t.jsxs)(a.Breadcrumbs,{sx:{fontSize:"14px",marginTop:"5px",marginBottom:"20px",...e},children:[n.map((e,a)=>(0,t.jsxs)("button",{type:"button",onClick:()=>{var t;return t=e.href,void l.push(t)},style:{display:"flex",alignItems:"center",gap:"5px",cursor:"pointer",background:"none",border:"none",padding:0,font:"inherit",color:"inherit"},children:[0===a&&(0,t.jsx)(r.default,{sx:{marginRight:"4px"}}),(0,t.jsx)("span",{children:e.name})]},e.href)),(0,t.jsx)("p",{style:{color:"#3AB549"},children:i})]})}o.propTypes={prevPaths:i.default.array.isRequired,current:i.default.string.isRequired,sx:i.default.object},e.s(["default",0,o])}]);