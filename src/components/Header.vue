<template>
    <div>
        <header>
            <h1>中国疫情变化</h1>
            <Time/>
        </header>
    </div>
</template>

<script>

    import Time from "@/components/Time";

    export default {
        name: "Header",
        components: {Time}
    }
</script>

<style scoped>
    header {
        position: relative;
        height: 1.25rem;
        background: url(../assets/images/head_bg.png) no-repeat top center;
        background-size: 100% 100%;
    }
    header h1 {
        font-size: 0.475rem;
        color: #fff;
        text-align: center;
        line-height: 1rem;
    }
</style>