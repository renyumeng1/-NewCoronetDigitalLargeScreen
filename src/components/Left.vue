<template>
    <div class="column">
        <PanelBar/>
        <PanelLine/>
        <PanelPie/>
    </div>
</template>

<script>
    import PanelBar from "@/components/LeftPanel/PanelBar";
    import PanelLine from "@/components/LeftPanel/PanelLine";
    import PanelPie from "@/components/LeftPanel/PanelPie";
    export default {
        name: "Left",
        components: {PanelPie, PanelLine, PanelBar},

    }
</script>

<style scoped>

</style>