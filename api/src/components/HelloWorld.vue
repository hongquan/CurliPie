<template>
  <div class="hello">

    <container xl="1200">
      <row>
        <column :xs='12' :lg="6" :lgShift="3">
          <vue-form :label-position="'top'">
            <vue-form-item>
              <vue-input v-model="curl" type='textarea' :rows='5' :placeholder="'curl params...'"></vue-input>
            </vue-form-item>
          </vue-form>
        </column>
      </row>
    </container>

    <h2>Result (<a href='/redoc'>API documentation</a>)</h2>
    <!-- Terminal widget from https://github.com/fobabs/ubuntu-terminal -->
    <section id="container">
      <div id="terminal">
        <!-- Terminal Bar -->
        <section id="terminal__bar">
          <div id="bar__buttons">
            <button class="bar__button" id="bar__button--exit">&#10005;</button>
            <button class="bar__button">&#9472;</button>
            <button class="bar__button">&#9723;</button>
          </div>
          <p id="bar__user">user@localhost: ~</p>
        </section>
        <!-- Terminal Body -->
        <section id="terminal__body">
          <div id="terminal__prompt">
            <span id="terminal__prompt--user">user@localhost:</span>
            <span id="terminal__prompt--location">~</span>
            <span id="terminal__prompt--bling">$</span>
          </div>
          <pre v-highlightjs="result.httpie"><code class='bash'></code></pre>
        </section>
      </div>
    </section>
    <ul class="errors">
      <li v-for="(e, i) of result.errors" :key="i">{{ e }}</li>
    </ul>
  </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
}
li {
  margin: 0 10px;
}
li:first-child {
  padding-top: 0.5rem;
}
li:last-child {
  padding-bottom: 0.5rem;
}
a {
  color: #42b983;
  text-decoration: none;
}
h2 {
  margin-top: 0;
}
.vue-form {
  width: 100%
}
.vue-form textarea {
  width: 100%;
  font-family: 'Courier New', Courier, monospace
}
code {
  font-size: large;
}
.errors {
  background-color: lightcoral;
  text-align: left;
}
.errors li {
  margin-top: 2px;
  margin-bottom: 2px;
}
#container {
  display: flex;
  justify-content: center;
  align-items: center;
}

#terminal {
  width: 70vw;
  height: 35vh;
  box-shadow: 2px 4px 10px rgba(0,0,0,0.5);
}

#terminal__bar {
  display: flex;
  width: 100%;
  height: 30px;
  align-items: center;
  padding: 0 8px;
  box-sizing: border-box;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  background: linear-gradient(#504b45 0%,#3c3b37 100%);
}

#bar__buttons {
  display: flex;
  align-items: center;
}

.bar__button {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  margin-right: 5px;
  font-size: 8px;
  height: 12px;
  width: 12px;
  box-sizing: border-box;
  border: none;
  border-radius: 100%;
  background: linear-gradient(#7d7871 0%, #595953 100%);
  text-shadow: 0px 1px 0px rgba(255,255,255,0.2);
  box-shadow: 0px 0px 1px 0px #41403A, 0px 1px 1px 0px #474642;
}
.bar__button:hover {
  cursor: pointer;
}
.bar__button:focus {
  outline: none;
}
#bar__button--exit {
  background: linear-gradient(#f37458 0%, #de4c12 100%);
  background-clip: padding-box;
}

#bar__user {
  color: #d5d0ce;
  margin-left: 6px;
  font-size: 14px;
  line-height: 15px;
}

#terminal__body {
  /* background: rgba(56, 4, 40, 0.9); */
  background: #232323;
  font-family: 'Ubuntu Mono';
  height: calc(100% - 30px);
  padding-top: 2px;
  margin-top: -1px;
}

#terminal__prompt {
  display: flex;
}
#terminal__prompt--user {
  color: #7eda28;
}
#terminal__prompt--location {
  color: #4878c0;
}
#terminal__prompt--bling {
  color: #dddddd;
}
#terminal__prompt--cursor {
  display: block;
  height: 17px;
  width: 8px;
  margin-left: 9px;
  animation: blink 1200ms linear infinite;
}
@keyframes blink {
  0% {
    background: #ffffff;
  }
  49% {
    background: #ffffff;
  }
  60% {
    background: transparent;
  }
  99% {
    background: transparent;
  }
  100% {
    background: #ffffff;
  }
}

@media (max-width: 600px) {
  #terminal {
    max-height: 90%;
    width: 90%;
  }
}
/* Custom */
pre .hljs {
  padding: 0;
  text-align: left;
  overflow-y: scroll;
  overflow-wrap: normal;
  overflow-x: unset;
  white-space: break-spaces;
}
</style>

<script>
import {Form, FormItem, Input} from 'vfc'

export default {
  name: 'HelloWorld',
  props: {
    msg: String,
  },
  components: {
    [Form.name]: Form,
    [FormItem.name]: FormItem,
    [Input.name]: Input
  },
  data () {
    return {
      curl: '',
      long_option: false,
      result: {
        httpie: '',
        errors: []
      }
    }
  },
  methods: {
    convertCurl () {
      var vm = this;
      const data = {curl: this.curl};
      fetch('/api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        vm.result = data;
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    },
  },
  watch: {
    curl () {
      this.debouncedConvert()
    }
  },
  created () {
    this.debouncedConvert = this._.debounce(this.convertCurl, 500)
  }
}
</script>
