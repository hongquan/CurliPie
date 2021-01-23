<template>
  <div class="home">
    <div>
      <img alt="Vue logo" src="https://www.nicepng.com/png/full/6-60631_pie-png.png" height="200px">
      <h1>Let's convert from <a href='https://curl.haxx.se'>cURL</a> to <a href='https://httpie.org'>HTTPie</a></h1>
    </div>
    <HelloWorld msg=""/>
  </div>
</template>

<style scoped>
h1 {
  display: inline-block;
  margin-left: 4px;
}
</style>

<script>
// @ is an alias to /src
import HelloWorld from '../components/HelloWorld.vue'

export default {
  name: 'home',
  props: ['form'],
  components: {
    HelloWorld
  }
}
</script>
