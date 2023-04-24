    Vue.component('button-counter', {
      data: function () {
        return {
          count: 0
        }
      },
      template: '<button v-on:click="count++" class="buttons">Счётчик кликов — {{ count }}</button>'
    })


          Vue.component('good-div', {
            props: ['good'],
            data: function () {
              return {
                quantity:0
              }
            },
            computed: {
              max_quantity: function () {
                return this.good.max_quantity;
              }
            }
            ,
            methods: {
              add_in_basket() {
                this.quantity++;
                if (this.quantity>this.max_quantity) {
                  this.quantity=this.max_quantity;
                  alert('Извините, больше на складе нет');
                }
              },
              remove_from_basket() {
                this.quantity--;
                if (this.quantity<0) {
                  this.quantity=0;
                }
              }
            },
            template: `
            <div class="block" id = "block">
              {{good.name}} <br>
              {{good.price}} руб. <br>
              В корзине: {{quantity}} шт. <br>
              <button v-on:click="add_in_basket">+</button>
              <button v-on:click="remove_from_basket">-</button>
            </div>
            `
          })


    var goodwrapper = new Vue({
      el:"#goodwrapper",
      data: {
        json: null,
        goods:[
          {name:'Холодильник', price:34000, max_quantity:10},
          {name:'Телевизор', price:12000, max_quantity:2},
          {name:'Микроволновая печь',price:18000, max_quantity:3},
          {name:'Микроволновая печь',price:18000, max_quantity:3},
          {name:'Холодильник', price:34000, max_quantity:10},
          {name:'Телевизор', price:12000, max_quantity:2}
        ]

        },
      methods: {
        async load_from_server()   {

          const requestOptions = {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.tutorial)
        }

        await  fetch("http://127.0.0.1:5000/api/good")
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            console.log(data);
            this.goods=data;
          });
        },
      },
      created: function() {
        this.load_from_server()}
      })
