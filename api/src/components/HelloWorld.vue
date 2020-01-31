<template>
  <div class="hello">
    <h1>Let's convert from <a href='https://curl.haxx.se'>cURL</a> to <a href='https://httpie.org'>HTTPie</a></h1>

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
    <pre v-highlightjs="result.httpie"><code class='bash'></code></pre>
  </div>
</template>

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
        console.log('Success:', data);
        vm.result = data;
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  },
  watch: {
    curl () {
      console.log('Changed'),
      this.debouncedConvert()
    }
  },
  created () {
    this.debouncedConvert = this._.debounce(this.convertCurl, 500)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
  text-decoration: none;
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
</style>
