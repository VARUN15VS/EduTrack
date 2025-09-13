const express = require('express')
const path = require('path')

const app = express()

app.set('views', path.join(__dirname, '../views'))
app.set('view engine', 'ejs')

app.get('/', (req, res) => {
    res.render('login')
})

app.listen(3000, () => {
    console.log("Server running at http://localhost:3000")
})
