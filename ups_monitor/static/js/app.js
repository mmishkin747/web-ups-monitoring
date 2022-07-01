

new Vue({
    el: '#state_ups',
    data: {
        ups_list:[]
    },
    created: function (){
        const vm = this;
        axios.get('/api/state_ups/')
        .then(function(response){
            vm.ups_list = response.data
            console.log(response.data)
        })
    }
});






