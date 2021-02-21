<template>
    <a href="#" class="float text-decoration-none">
        <i class="fa fa-plus my-float"></i>
        Volver
    </a>
</template>

<script>
export default {
  name: 'FloatingButton',
  props: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.float{
	position:fixed;
	width:60px;
	height:60px;
	bottom:40px;
	right:40px;
	background-color:#0C9;
	color:#FFF;
	border-radius:50px;
	text-align:center;
	box-shadow: 2px 2px 3px #999;
}

.my-float{
	margin-top:22px;
}
</style>
