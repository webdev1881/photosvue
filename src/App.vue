<template>
  <div id="app">
    <div>
    <ul class="list" v-for="(i, index) in json" :key="i">
      <div class="li">
        <div class="title">
          {{ index+1 }}.  
           Наш Артикул: {{ i.article }} - <b>{{ i.name }} </b>
        </div>
        <div v-for="(img, index) in i.images" :key="index" class="imgs">
          <div v-if="index !== 0" class="nom">
            {{ index }}
          </div>
          <img v-if="index !== 0" :src="img" alt="" class="img">
          <!-- v-if="index % 2 === 1" -->
        </div>
      </div>
    </ul>
  </div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import json from './results.json'
export default {
  name: 'App',
  components: {
    HelloWorld
  },
  data() {
    return {
      json
    }
  }
}
</script>

<style>

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
.list {
  display: flex;
  list-style-type: none;
}

.li {
  display: flex;
  align-items: center;
  justify-content: center;
}
.img {
  display: flex;
  /* width: 100px; */
  height: 100px;
  margin: 0 10px;
}
.imgs {
  display: flex;
  align-items: center;
}
.title {
  width: max-content;
  margin-right: 10px;
}
:root {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light;
  /* color: rgba(255, 255, 255, 0.87); */
  background-color: rgb(219, 217, 217);

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  display: flex;
  /* place-items: center; */
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1.1;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  background-color: gray;
  cursor: pointer;
  transition: border-color 0.25s;
}
button:hover {
  border-color: #646cff;
}
button:focus,
button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

.card {
  padding: 2em;
}

#app {
  max-width: 1280px;
  /* margin: 0 auto; */
  padding: 2rem;
  text-align: center;
}

@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
  }
  a:hover {
    color: #747bff;
  }
  button {
    background-color: #f9f9f9;
  }
}

</style>
