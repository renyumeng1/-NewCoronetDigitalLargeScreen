<template>
    <div class="column">
        <PanelBar/>
        <PanelLine/>
        <Shuffling/>
    </div>
</template>

<script>
import PanelBar from "@/components/LeftPanel/PanelBar";
import PanelLine from "@/components/LeftPanel/PanelLine";
import Shuffling from '@/components/LeftPanel/Shuffling'

export default {
    name: "Left",
    components: {Shuffling, PanelLine, PanelBar},


}
</script>

<style scoped>

</style>