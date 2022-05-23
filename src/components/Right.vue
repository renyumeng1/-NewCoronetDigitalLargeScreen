<template>
    <div class="column">
        <Top/>
<!--        <PanelLine/>-->
        <PanelPie/>

    </div>
</template>

<script>
    import Top from "@/components/RightPanel/Top";
    import PanelPie from "@/components/RightPanel/PanelPie";
    export default {
        name: "Right",
        components: {PanelPie, Top},
    }
</script>

<style scoped>

</style>