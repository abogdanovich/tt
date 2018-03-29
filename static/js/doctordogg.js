var DD = function() {
   var _ = {
        l: function(obj, objName) {
            if(typeof objName === 'string') {
                console.log(objName);
            } else {
                console.log('[noname]');
            }
            console.log(typeof obj);
            console.log(obj);
            console.log(']');
        }
   }

   if(typeof arguments[0] !== 'undefined') {
       if(typeof _[arguments[0]] !== 'undefined') {
            return _[arguments[0]];
       }
   }

};

DD();

