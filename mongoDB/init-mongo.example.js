db.createUser(
	{
		user  : "yourUsername",
		pwd   : "your password",
		roles : [
			  {
				role : "readWrite",
				db   : "database-name"
			  }
		]
	}
)
