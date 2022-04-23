<template>
    <div class="column">
        <PanelBar/>
        <PanelLine/>
        <PanelPie/>

    </div>
</template>

<script>
    import PanelBar from "@/components/RightPanel/PanelBar";
    import PanelLine from "@/components/RightPanel/PanelLine";
    import PanelPie from "@/components/RightPanel/PanelPie";
    export default {
        name: "Right",
        components: {PanelPie, PanelLine, PanelBar},
    }
</script>

<style scoped>

</style>