require('dotenv').config();

module.exports = {
  clientId: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,
  redirectUri: process.env.REDIRECT_URI,
  refreshToken: process.env.REFRESH_TOKEN,
  emailUser: process.env.EMAIL_USER

};
