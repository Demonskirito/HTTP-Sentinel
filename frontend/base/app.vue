<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue"

const API_BASE = "http://127.0.0.1:8000"

const history = ref([])
const selected = ref(null)
const loading = ref(false)
const error = ref("")

const searchText = ref("")
const methodFilter = ref("ALL")

let timer = null

async function loadHistory() {
  try {
    loading.value = true
    error.value = ""

    const response = await fetch(
      `${API_BASE}/api/history?limit=200`
    )

    if (!response.ok) {
      throw new Error(
        `HTTP ${response.status}`
      )
    }

    const result = await response.json()

    history.value = result.data || []

    // 如果当前已经选中了请求，刷新后重新获取详情
    if (selected.value) {
      const exists = history.value.find(
        item => item.id === selected.value.id
      )

      if (exists) {
        await selectRequest(exists)
      }
    }

  } catch (e) {
    console.error("Failed to load history:", e)
    error.value = e.message
  } finally {
    loading.value = false
  }
}


async function selectRequest(item) {
  try {
    const response = await fetch(
      `${API_BASE}/api/history/${item.id}`
    )

    if (!response.ok) {
      throw new Error(
        `HTTP ${response.status}`
      )
    }

    const result = await response.json()

    selected.value = result.data

  } catch (e) {
    console.error(
      "Failed to load request detail:",
      e
    )

    error.value = e.message
  }
}


function formatTime(timestamp) {
  if (!timestamp) {
    return "-"
  }

  return new Date(
    timestamp * 1000
  ).toLocaleTimeString()
}


function formatSize(size) {
  if (size === undefined || size === null) {
    return "-"
  }

  if (size < 1024) {
    return `${size} B`
  }

  if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(1)} KB`
  }

  return `${(size / 1024 / 1024).toFixed(1)} MB`
}


function formatHeaders(headers) {
  if (!headers) {
    return ""
  }

  return Object.entries(headers)
    .map(([key, value]) => `${key}: ${value}`)
    .join("\n")
}


const filteredHistory = computed(() => {

  const keyword =
    searchText.value
      .trim()
      .toLowerCase()

  return history.value.filter(item => {

    const methodMatch =
      methodFilter.value === "ALL" ||
      item.method === methodFilter.value

    const searchMatch =
      !keyword ||
      (item.url || "")
        .toLowerCase()
        .includes(keyword)

    return methodMatch && searchMatch
  })
})


function statusClass(status) {

  if (!status) {
    return ""
  }

  if (status >= 200 && status < 300) {
    return "status-success"
  }

  if (status >= 300 && status < 400) {
    return "status-redirect"
  }

  if (status >= 400 && status < 500) {
    return "status-client-error"
  }

  if (status >= 500) {
    return "status-server-error"
  }

  return ""
}


function clearSelection() {
  selected.value = null
}


onMounted(() => {

  loadHistory()

  timer = setInterval(
    loadHistory,
    2000
  )
})


onUnmounted(() => {

  if (timer) {
    clearInterval(timer)
  }

})
</script>


<template>

  <div class="app">

    <!-- Header -->

    <header class="topbar">

      <div class="logo">
        AI-WebSec-Assistant
      </div>

      <div class="proxy-status">

        <span class="status-dot"></span>

        Proxy

        <code>127.0.0.1:8080</code>

        <span class="running">
          RUNNING
        </span>

      </div>

      <button
        class="refresh-btn"
        @click="loadHistory"
      >
        ↻ Refresh
      </button>

    </header>


    <!-- Toolbar -->

    <div class="toolbar">

      <input
        v-model="searchText"
        class="search"
        placeholder="Filter URL..."
      />

      <select
        v-model="methodFilter"
        class="method-select"
      >
        <option value="ALL">
          All Methods
        </option>

        <option value="GET">
          GET
        </option>

        <option value="POST">
          POST
        </option>

        <option value="PUT">
          PUT
        </option>

        <option value="PATCH">
          PATCH
        </option>

        <option value="DELETE">
          DELETE
        </option>
      </select>

      <div class="request-count">

        {{ filteredHistory.length }}
        requests

      </div>

    </div>


    <!-- Error -->

    <div
      v-if="error"
      class="error"
    >
      {{ error }}
    </div>


    <!-- Main -->

    <main class="main">

      <!-- History -->

      <section class="history-panel">

        <div class="panel-title">

          HTTP History

          <span>
            {{ filteredHistory.length }}
          </span>

        </div>


        <div class="table-header">

          <div>#</div>
          <div>Method</div>
          <div>URL</div>
          <div>Status</div>
          <div>Type</div>
          <div>Size</div>
          <div>Time</div>

        </div>


        <div
          v-if="filteredHistory.length === 0"
          class="empty"
        >
          No HTTP requests
        </div>


        <div
          v-for="(item, index) in filteredHistory"
          :key="item.id"
          class="history-row"
          :class="{
            selected:
              selected?.id === item.id
          }"
          @click="selectRequest(item)"
        >

          <div class="index">
            {{ index + 1 }}
          </div>

          <div
            class="method"
            :class="`method-${item.method}`"
          >
            {{ item.method }}
          </div>

          <div class="url">

            <div class="host">
              {{ item.host }}
            </div>

            <div class="path">
              {{ item.path }}
            </div>

          </div>

          <div
            class="status"
            :class="statusClass(
              item.status_code
            )"
          >
            {{ item.status_code || "-" }}
          </div>

          <div class="type">

            {{
              item.content_type
                ?.split(";")[0]
                || "-"
            }}

          </div>

          <div class="size">

            {{ formatSize(
              item.response_size
            ) }}

          </div>

          <div class="time">

            {{ formatTime(
              item.timestamp
            ) }}

          </div>

        </div>

      </section>


      <!-- Inspector -->

      <section class="inspector">

        <div
          v-if="!selected"
          class="inspector-empty"
        >

          <div class="big-icon">
            ⇦
          </div>

          <div>
            Select a request
          </div>

          <small>
            Request / Response details
            will appear here
          </small>

        </div>


        <div
          v-else
          class="inspector-content"
        >

          <div class="detail-header">

            <div>

              <span
                class="detail-method"
                :class="`method-${selected.request.method}`"
              >
                {{ selected.request.method }}
              </span>

              <span class="detail-url">

                {{ selected.request.url }}

              </span>

            </div>

            <button
              class="close-btn"
              @click="clearSelection"
            >
              ×
            </button>

          </div>


          <!-- Request -->

          <div class="detail-section">

            <div class="section-title">
              REQUEST
            </div>

            <pre class="http-content"><span class="request-line">{{ selected.request.method }} {{ selected.request.path }} HTTP/1.1</span>
{{ formatHeaders(selected.request.headers) }}

{{ selected.request.body || "" }}</pre>

          </div>


          <!-- Response -->

          <div class="detail-section">

            <div class="section-title response-title">

              RESPONSE

              <span
                class="response-status"
                :class="statusClass(
                  selected.response?.status_code
                )"
              >
                {{ selected.response?.status_code }}
              </span>

            </div>

            <pre class="http-content">{{ selected.response?.status_code ? `HTTP/1.1 ${selected.response.status_code}` : "" }}
{{ formatHeaders(selected.response?.headers) }}

{{ selected.response?.body || "" }}</pre>

          </div>

        </div>

      </section>

    </main>

  </div>

</template>


<style scoped>

* {
  box-sizing: border-box;
}

.app {
  height: 100vh;
  background: #101214;
  color: #d7d9dc;
  font-family:
    Consolas,
    "Courier New",
    monospace;

  display: flex;
  flex-direction: column;
}


/* Header */

.topbar {
  height: 52px;
  display: flex;
  align-items: center;
  padding: 0 18px;

  background: #181b1f;

  border-bottom:
    1px solid #30343a;
}

.logo {
  font-size: 17px;
  font-weight: bold;
  color: #f0f0f0;
}

.proxy-status {
  margin-left: 35px;

  display: flex;
  align-items: center;

  gap: 8px;

  font-size: 12px;

  color: #aaa;
}

.proxy-status code {
  color: #ddd;
}

.status-dot {
  width: 8px;
  height: 8px;

  border-radius: 50%;

  background: #44d17a;
}

.running {
  color: #44d17a;
}

.refresh-btn {
  margin-left: auto;

  background: #262a2f;
  color: #ddd;

  border:
    1px solid #3a3f46;

  padding:
    6px 12px;

  border-radius: 4px;

  cursor: pointer;
}

.refresh-btn:hover {
  background: #30353b;
}


/* Toolbar */

.toolbar {
  height: 48px;

  display: flex;
  align-items: center;

  gap: 10px;

  padding: 0 12px;

  background: #141619;

  border-bottom:
    1px solid #30343a;
}

.search {
  width: 300px;

  background: #0d0f11;

  border:
    1px solid #363a40;

  color: #ddd;

  padding:
    7px 10px;

  border-radius: 3px;

  outline: none;
}

.search:focus {
  border-color: #667085;
}

.method-select {
  background: #0d0f11;

  border:
    1px solid #363a40;

  color: #ddd;

  padding: 7px;

  border-radius: 3px;
}

.request-count {
  margin-left: auto;

  color: #777;

  font-size: 12px;
}


/* Main */

.main {
  flex: 1;

  min-height: 0;

  display: flex;
}


/* History */

.history-panel {
  width: 52%;

  min-width: 600px;

  border-right:
    1px solid #30343a;

  overflow-y: auto;
}

.panel-title {
  height: 38px;

  display: flex;
  align-items: center;

  padding: 0 12px;

  font-size: 12px;

  font-weight: bold;

  color: #aaa;

  border-bottom:
    1px solid #30343a;
}

.panel-title span {
  margin-left: 7px;

  color: #666;
}


.table-header,
.history-row {
  display: grid;

  grid-template-columns:
    38px
    65px
    minmax(250px, 1fr)
    65px
    120px
    75px
    85px;

  align-items: center;
}

.table-header {
  height: 32px;

  padding: 0 8px;

  background: #1a1d21;

  color: #777;

  font-size: 11px;

  position: sticky;

  top: 0;

  z-index: 2;
}

.history-row {
  min-height: 48px;

  padding: 5px 8px;

  border-bottom:
    1px solid #202328;

  font-size: 12px;

  cursor: pointer;
}

.history-row:hover {
  background: #191d21;
}

.history-row.selected {
  background: #242a31;
}

.index {
  color: #555;
}

.method {
  font-weight: bold;
}

.method-GET {
  color: #4ea1ff;
}

.method-POST {
  color: #d9a441;
}

.method-PUT {
  color: #c58cff;
}

.method-PATCH {
  color: #c58cff;
}

.method-DELETE {
  color: #f07178;
}

.url {
  overflow: hidden;
}

.host {
  color: #ddd;

  white-space: nowrap;

  overflow: hidden;

  text-overflow: ellipsis;
}

.path {
  margin-top: 3px;

  color: #666;

  white-space: nowrap;

  overflow: hidden;

  text-overflow: ellipsis;
}

.status-success {
  color: #48c774;
}

.status-redirect {
  color: #e0ad4f;
}

.status-client-error {
  color: #f08a8a;
}

.status-server-error {
  color: #ff5f56;
}

.type {
  color: #888;

  white-space: nowrap;

  overflow: hidden;

  text-overflow: ellipsis;
}

.size,
.time {
  color: #666;
}

.empty {
  padding: 40px;

  text-align: center;

  color: #555;
}


/* Inspector */

.inspector {
  flex: 1;

  min-width: 0;

  overflow: hidden;
}

.inspector-empty {
  height: 100%;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  gap: 10px;

  color: #666;
}

.big-icon {
  font-size: 40px;

  color: #444;
}

.inspector-empty small {
  color: #444;
}


.inspector-content {
  height: 100%;

  overflow-y: auto;
}

.detail-header {
  min-height: 52px;

  padding: 10px 14px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  border-bottom:
    1px solid #30343a;

  background: #181b1f;
}

.detail-method {
  font-weight: bold;

  margin-right: 12px;
}

.detail-url {
  color: #ddd;

  word-break: break-all;

  font-size: 12px;
}

.close-btn {
  background: none;

  border: none;

  color: #777;

  font-size: 22px;

  cursor: pointer;
}

.close-btn:hover {
  color: #fff;
}


/* Detail */

.detail-section {
  border-bottom:
    1px solid #30343a;
}

.section-title {
  height: 34px;

  display: flex;

  align-items: center;

  padding: 0 12px;

  background: #15181b;

  color: #777;

  font-size: 11px;

  font-weight: bold;
}

.response-title {
  gap: 10px;
}

.response-status {
  font-size: 12px;
}

.http-content {
  margin: 0;

  padding: 14px;

  background: #0c0e10;

  color: #bfc4ca;

  font-family:
    Consolas,
    "Courier New",
    monospace;

  font-size: 12px;

  line-height: 1.55;

  white-space: pre-wrap;

  word-break: break-word;

  min-height: 100px;

  max-height: 500px;

  overflow: auto;
}

.request-line {
  color: #64a8ff;
}


/* Error */

.error {
  padding: 8px 14px;

  background: #321b1b;

  border-bottom:
    1px solid #653333;

  color: #ff8c8c;

  font-size: 12px;
}

</style>
