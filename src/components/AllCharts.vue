<template>
    <div>
        <section class="mainbox">
            <Left/>
            <Middle/>
            <Right/>
        </section>

    </div>
</template>

<script>
    import Left from "@/components/Left";
    import Middle from "@/components/Middle";
    import Right from "@/components/Right";

    export default {
        name: "Section",
        components: {Right, Middle, Left}
    }
</script>

<style scoped>
    .mainbox {
        min-width: 1024px;
        max-width: 1920px;
        padding: 0.125rem 0.125rem 0;
        display: flex;
    }

    .mainbox .column {
        flex: 3;
    }

    .mainbox .column:nth-child(2) {
        flex: 5;
        margin: 0 0.125rem 0.1875rem;
        overflow: hidden;
    }
</style>