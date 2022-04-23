<template>
    <div class="column">
        <Total/>
        <Map/>
    </div>
</template>

<script>
    import Total from "@/components/MiddlePanel/Total";
    import Map from "@/components/MiddlePanel/Map";
    export default {
        name: "Middle",
        components: {Map, Total}
    }
</script>

<style scoped>

</style>