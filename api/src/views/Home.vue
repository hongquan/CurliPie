<template>
  <div class="home">
    <img alt="Vue logo" src="https://www.nicepng.com/png/full/6-60631_pie-png.png" height="200px">
    <HelloWorld msg=""/>
  </div>
</template>

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
