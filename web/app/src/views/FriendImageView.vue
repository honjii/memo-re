<template>
  <div class="flex relative">
    <div class="fixedGlobal">
      <GlobalHeader />
    </div>
    <div class="preOWrap">
      <div class="flex preOverWrap">
        <div class="preWrap">
          <div class="flex innerWrap">
            <p class="title">{{ title }}</p>
          </div>
          <ul class="flex" style="flex-wrap: wrap;">
            <li v-for="word in keyword" v-bind:key="word" class="keyword" style=" margin-bottom: 6px;">
              {{ word }}
            </li>
          </ul>
          <p class="text_uri">{{ text_uri }}</p>
        </div>
        <div class="preImg">
          <img :src="image_uri" alt="画像" />
          <p class="time">{{ time[0] }}</p>
        </div>
      </div>
      <button @click="GiveImageModal()">この画像をもらう</button>
      <div class="scrWrap">
        <ul class="flex">
          <li
            v-for="img in scrollData"
            v-bind:key="img"
            class="scrImg"
            @click="ImageView(img.id, img.title, img.keyword,img.image_uri, img.text_uri, img.is_public, img.created_at)"
          >
            <img :src="ImgSrc(img.image_uri)" alt="画像" />
            <p class="opacity">{{ img.title }}</p>
          </li>
        </ul>
      </div>
    </div>
    <div v-if="modalFlag == true" class="absolute modal">
      <div class="modalContent">
        <h2>共有申請しますか？</h2>
        <img :src="image_uri" alt="画像" />
        <p v-if="errorFlag == true">すでに相手から申請が来ています</p>
        <div class="flex button">
          <button class="cancel" @click="Cancel()">キャンセル</button>
          <button class="accept" @click="Share()">申請</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_SERVER, IMG_URL } from "@/assets/config.js";
import GlobalHeader from "@/components/GlobalHeader.vue";
export default {
  name: "ImageView",
  data() {
    return {
      id: localStorage.getItem("friendNoteId"),
      keyword: localStorage.getItem("friendNoteKeyword").split(","),
      title: localStorage.getItem("friendNoteTitle"),
      image_uri: IMG_URL + localStorage.getItem("friendNoteImage"),
      user: localStorage.getItem("friendNoteUser"),
      text_uri: localStorage.getItem("friendNoteText"),
      data: [],
      scrollData: [],
      keywordAry: "",
      is_public: null,
      modalFlag: false,
      errorFlag: false,
      time: "",
    };
  },
  components: {
    GlobalHeader,
  },
  methods: {
    GiveImageModal: async function () {
      this.modalFlag = true;
    },
    ScrollData: async function () {
      const userId = localStorage.getItem("friendId");
      const token = this.$cookies.get("access");
      await axios
        .get(API_SERVER + "/api/v1/brains/friends/" + userId +"/", {
          headers: { Authorization: "JWT " + token },
        })
        .then((response) => {
          this.scrollData = response.data;
          //console.log(this.scrollData);
          return;
        })
        .catch((e) => {
          console.log(e);
          return;
        });
    },
    ImgSrc(img_uri) {
      const img = IMG_URL + img_uri;
      return img;
    },
    ImageView(noteId,title,keyword,img_uri, text_uri, is_public, time) {
      //console.log("click");
      localStorage.setItem("noteId", noteId);
      this.title = title;
      this.keyword = keyword.split(",");
      this.image_uri = IMG_URL + img_uri;
      this.text_uri = text_uri;
      this.is_public = is_public;
      this.time = time.split("T");
    },
    Public: async function (flag) {
      if (flag === 0) {
        this.is_public = false;
      } else {
        this.is_public = true;
      }
      const requestBody = {
        is_public: this.is_public,
      };
      const noteId = localStorage.getItem("noteId");
      const token = this.$cookies.get("access");
      // .post(API_SERVER + "/api/v1/brains/" + this.user, requestBody, {
      await axios
        .patch(API_SERVER + "/api/v1/brains/" + noteId + "/", requestBody, {
          headers: { Authorization: "JWT " + token },
        })
        .then(() => {
          console.log("成功");
          return;
        })
        .catch((e) => {
          console.log(e);
          return;
        });
    },
    Cancel() {
      this.modalFlag = !this.modalFlag;
    },
    //申請
    Share() {
      const requestBody = {
        user_from: parseInt(this.user),
        note: parseInt(this.id),
        get: true,
      };
      console.log(requestBody);
      const token = this.$cookies.get("access");
      axios
        .post(API_SERVER + "/api/v1/brains/share/", requestBody, {
          headers: { Authorization: "JWT " + token },})
        .then(() => {
          console.log("成功");
          this.modalFlag = !this.modalFlag;
          return;
        })
        .catch(() => {
          this.errorFlag = true;
        });
    },
  },
  created() {
    if (this.$cookies.get("access") === null) {
      const refresh = this.$cookies.get("refresh");
      if (refresh != null) {
        console.log("リフレッシュ");
        const requestBody = {
          refresh: refresh,
        };
        axios
          .post(API_SERVER + "/api/v1/auth/jwt/refresh/", requestBody)
          .then((response) => {
            let token = response.data.access;
            this.$cookies.set("access", token, 60 * 30);
            location.reload();
          })
          .catch(() => {
            //エラー回避用
            this.$router.push("/SignIn");
          });
      }else{
        this.$router.push("/SignIn");
      }
      return;
    }
    this.time = localStorage.getItem("friendTime").split("T");
    // this.ImageData();
    this.ScrollData();
  },
};
</script>

<style scoped>
.preOWrap {
  margin: 0 auto;
  padding-top: 100px;
  width: 900px;
}
.preOverWrap {
  justify-content: space-between;
  flex-wrap: wrap;
}
.preWrap {
  width: 400px;
}
.innerWrap {
  justify-content: space-between;
  flex-wrap: wrap;
}
.title {
  width: 200px;
  overflow-wrap: break-word;
  font-size: 28px;
  font-weight: bolder;
}
.public {
  font-weight: bolder;
  line-height: 32px;
  cursor: pointer;
}
.text_uri {
  font-size: 18px;
}
.keyword {
  color: #fff;
  font-size: 16px;
  background: #6d8dff;
  padding: 4px 8px;
  margin-right: 10px;
  border-radius: 5px;
}
.text_uri {
  width: 400px;
  word-wrap: break-word;
  margin-top: 60px;
  line-height: 24px;
}
.preImg {
  width: 360px;
}
.preImg img {
  width: 100%;
  border-radius: 20px;
  box-shadow: 3px 4px 8px 2px rgb(75, 75, 75);
}
.scrWrap {
  margin-top: 60px;
}
.scrWrap ul {
  width: 900px;
  flex-wrap: wrap;
}
button {
  margin-top: 40px;
  color: #fff;
  background: #ff78f4;
  padding: 10px 26px;
  border-radius: 10px;
  box-shadow: 1px 2px 1px 1px rgb(194, 194, 194);
}
button:hover{
  background: #ff32b1;
}

.scrImg {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 15px;
  cursor: pointer;
  box-shadow: 8px 6px 8px 3px #999;
}
.scrImg img {
  width: 150px;
}
.scrImg p {
  font-size: 12px;
  width: 150px;
  height: 150px;
  text-align: center;
  line-height: 150px;
  font-weight: bold;
  color: #fff;
  background: rgba(0, 0, 0, 0.4);
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
}
.scrImg p:hover {
  opacity: 1;
  transition: 0.6s;
}
.modal {
  background: rgba(255, 255, 255, 0.4);
  width: calc(100% - 170px);
  height: 100vh;
  left: 170px;
}
.modalContent {
  width: 420px;
  height: 500px;
  background: #fff;
  filter: drop-shadow(0px 0px 20px #aaa);
  margin: 60px auto 0;
  border-radius: 20px;
  padding-top: 40px;
}
.modalContent h2 {
  font-size: 24px;
  font-weight: bolder;
  text-align: center;
  margin-bottom: 20px;
  color: #666;
}
.modalContent img {
  display: block;
  width: 200px;
  height: 200px;
  margin: 0 auto;
}
.button {
  width: 340px;
  margin: 0 auto;
  justify-content: space-between;
}
.modalContent button {
  float: right;
  color: #fff;
  width: 160px;
  height: 54px;
  text-align: center;
  border-radius: 5px;
  box-shadow: 4px 4px 8px 3px #bbb;
}
.cancel {
  background: #ff78f4;
}
.cancel:hover {
  background: #ff32b1;
}
.accept {
  background: #1e4fff;
}
.accept:hover {
  background: #0015ff;
}
.modalContent .accept:hover {
  background: #7b98ff;
}
.modalContent p {
  margin-top: 20px;
  text-align: center;
  font-size: 16px;
}
.time {
  margin-top: 10px;
  font-weight: bold;
  text-align: end;
}
</style>
