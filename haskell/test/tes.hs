-- Define the route type as a String (it could be a regular expression in a more advanced version)
type Route = String

-- Define the handler type as a function that takes a request and returns a response (String for simplicity)
type Handler = String -> String

-- The router type is a function that takes a route and returns a handler
type Router = Route -> Maybe Handler
