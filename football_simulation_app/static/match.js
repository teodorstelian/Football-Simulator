const el = document.querySelector('.app');
const mu = 'https://upload.wikimedia.org/wikipedia/ru/thumb/7/7a/Manchester_United_FC_crest.svg/250px-Manchester_United_FC_crest.svg.png';
const bar = 'http://abali.ru/wp-content/uploads/2014/05/emblema_fk_barselona_barcelona-150x150.png';
const audioSrc = 'https://files.hsmedia.ru/elle/uploaded/e94fa8a1ea26520_1580227911.mp3';

const timeout = 3500;

if (!el) {
  throw new Error('App container not found :(');
}

const app = new Vue({
  el,
  data() {
    return {
      audioSrc,
      logos: { mu, bar },
      animation: false };

  },
  methods: {
    launch() {
      if (this.animation) {
        return;
      }

      this.animation = true;
      this.$refs.audio.play();
      setTimeout(() => {
        this.animation = false;
      }, timeout);
    } } });