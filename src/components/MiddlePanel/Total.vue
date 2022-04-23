<template>
    <div class="no">
        <div class="no-hd">
            <ul>
                <li>125811</li>
                <li>104563</li>
            </ul>
        </div>
        <div class="no-bd">
            <ul>
                <li>前端需求人数</li>
                <li>市场供应人数</li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Total"
    }
</script>

<style scoped>
    .no {
        background: rgba(101, 132, 226, 0.1);
        padding: 0.1875rem;
    }

    .no .no-hd {
        position: relative;
        border: 1px solid rgba(25, 186, 139, 0.17);
    }

    .no .no-hd::before {
        content: "";
        position: absolute;
        width: 30px;
        height: 10px;
        border-top: 2px solid #02a6b5;
        border-left: 2px solid #02a6b5;
        top: 0;
        left: 0;
    }

    .no .no-hd::after {
        content: "";
        position: absolute;
        width: 30px;
        height: 10px;
        border-bottom: 2px solid #02a6b5;
        border-right: 2px solid #02a6b5;
        right: 0;
        bottom: 0;
    }

    .no .no-hd ul {
        display: flex;
    }

    .no .no-hd ul li {
        position: relative;
        flex: 1;
        text-align: center;
        height: 1rem;
        line-height: 1rem;
        font-size: 0.875rem;
        color: #ffeb7b;
        padding: 0.05rem 0;
        font-family: electronicFont;
        font-weight: bold;
    }

    .no .no-hd ul li:first-child::after {
        content: "";
        position: absolute;
        height: 50%;
        width: 1px;
        background: rgba(255, 255, 255, 0.2);
        right: 0;
        top: 25%;
    }

    .no .no-bd ul {
        display: flex;
    }

    .no .no-bd ul li {
        flex: 1;
        height: 0.5rem;
        line-height: 0.5rem;
        text-align: center;
        font-size: 0.225rem;
        color: rgba(255, 255, 255, 0.7);
        padding-top: 0.125rem;
    }
</style>