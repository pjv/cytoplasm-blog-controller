import os, cytoplasm 

class Post(object):
    "A sort-of file-like object that defines a post."
    def __init__(self, path):
        self.path = path
        # The following are to be deduced somehow from metadata; they don't do anything yet.
        self.date = None
        self.contents = None
        self.title = None
        # Interpret the file.
        cytoplasm.interpreters.interpret(self.path, self)

    def close(self):
        # This is just here so that python doesn't throw up an error when something else thinks
        # this is a file.
        pass

    def write(self, s):
        # instead of writing to disk, simply change the contents attribute.
        self.contents = s 

class BlogController(cytoplasm.controllers.Controller):
    def __init__(self, data, destination, templates="_templates/"):
        # take three arguments: the source directory, the destination directory, and, optionally,
        # a directory wherein the templates reside.
        self.templates_directory = templates
        cytoplasm.controllers.Controller.__init__(self, data, destination)
        
    def __call__(self):
        post_template = "%s/%s" %(self.templates_directory, "post.mako")
        for post in os.listdir(self.data_directory):
            this_post = Post("%s/%s" %(self.data_directory, post))
            destination = "%s/%s" %(self.destination_directory, "post.html")
            cytoplasm.interpreters.interpret(post_template, destination, post=this_post)

info = { "class" : BlogController }
