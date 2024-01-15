import github
from utils import *
import env
import os

def write_gitignore_file(dir):
    dir = os.path.expanduser(dir)
    assert(is_dir(dir))

    def infer_filetype_from_directory_files(dir):
        files = os.listdir(dir)
        extensions = [get_extension(file) for file in files]
        src = tally(extensions)
        winner = max(src, key = src.get)
        filetype = variables.filetype_aliases.get(winner, winner)
        return filetype

    filetype = infer_filetype_from_directory_files(dir)
    patterns = variables.git_ignore_patterns.get(filetype)
    if patterns:
        write(".gitignore", join(patterns), dir = dir)

class Github:
    
    def view(self, path='', file=''):
        contents = self.getRepoContents(path=path)
        if file:
            f = lambda x: tail(x.path) == tail(file)
            content = find(contents, f)
            if content:
                blue_colon('text', content.decoded_content.decode('utf-8'))
                blue_colon('content', content)
                blue_colon('path', content.path)
            else:
                print('no content found')
                print('original contents:')
                pprint(contents)
        else:
            pprint(contents)
    

    def __init__(self, key=None):
        self.token = env.github_token_ref[key]
        self.github = github.Github(self.token)
        self.user = self.github.get_user()
        self.username = self.user.login

    def doAuthentication(self, repoName):
        command = (
            'curl -H "Authorization: token '
            + self.token
            + '" --data \'{"name":"'
            + repoName
            + "\"}' https://api.github.com/user/repos"
        )
        os.system(command)
        blue_colon('Authenticated', repoName)

    def setRepo(self, repoName, private=False, create=False):

        if '/' in repoName:
            repoName = repoName.split('/')[-1]

        try:
            self.repo = self.user.get_repo(repoName)
        except Exception as e:
            if not create:
                raise Exception('The repo doesnt exist and create is False')

            try:
                self.repo = self.user.create_repo(
                    repoName, private=private
                )
            except Exception as e:
                if test(str(e), "Repository creation failed"):
                    raise e

                self.doAuthentication(repoName)
                sleep(1)
                self.repo = self.github.get_repo(repoName)

        blue_colon('Successfully set the repo', repoName)
        return self.repo

    def getRepoContents(self, repo=None, path='', recursive = 0):
        if not repo: 
            repo = self.repo

        try:
            ref = repo.default_branch
            contents = repo.get_contents(path, ref=ref)
            if not recursive:
                return contents

            store = []
            while contents:
                content = contents.pop(0)
                if is_private_filename(content.path):
                    continue
                if content.type == "dir":
                    items = repo.get_contents(content.path, ref=ref)
                    contents.extend(items)
                else:
                    store.append(content)
            return store

        except Exception as e:
            raise e

    def getRepo(self, x):
        return self.user.get_repo(x) if is_string(x) else x

    def getRepos(self):
        return self.user.get_repos()
    
    def open_url(self):
        view(self.repo.html_url)
    

class GithubController(Github):
    def view_repos(self):
        repos = self.getRepos()

        def runner():
            repo = choose(repos)
            if repo:
                contents = self.getRepoContents(repo)
                print(repo)
                pprint(contents)
                press_anything_to_continue()
                runner()
        
        runner()


    def deleteRepo(self, x):
        repo = self.getRepo(x)

        if test('kdog3682|2023', repo.name):
            if not test('kdog3682-', repo.name):
                return red('Forbidden Deletion', repo.name)

        repo.delete()
        blue_colon('Deleting Repo', repo.name)
        localName = re.sub('kdog3682-', '', repo.name)
        localDir = npath(rootdir, localName)
        rmdir(localDir, ask=True)


    def upload_file(self, file, content=None, name = None):
         return update_repo(self.repo, file, content, name = name)

    def upload_directory(self, dir, name = None):
        files = os.listdir(dir)
        dirname = head(dir)
        for file in files:
            p = Path(dir, file)
            if p.is_dir():
                continue

            content = pprint().read_bytes()
            name = str(Path(dirname, file))
            update_repo(self.repo, content = content, name = path)
    

    def initialize_local_directory(self, dir):
        """
            turns the given directory into a git repo
            optionally writes gitignore 
            based on the files present in the directory
        """

        dir = os.path.expanduser(dir)
        if is_git_directory(dir):
             panic("dir: $dir is already a git repository")

        if not is_dir(dir):
            answer = inform("""
                $dir is not an existant directory
                would you like to create it?
            """, accept_on_enter = 1)
            if not answer:
                return 
            else:
                mkdir(dir)

        green("starting initialization process for $dir")
        repo_name = ask("repo_name", tail(dir))
        address = f"{self.username}/{repo_name}"
        repository = self.setRepo(repo_name, create = True)
        assertion(repository, message = "no repository was found for $repo_name")

        system_command(f"""
            cd {dir}
            git init
            git add .
            git commit -m "first commit"
            git branch -M main
            git remote add origin git@github.com:{address}.git
            git push -u origin main 
        """, confirm = 1)

        write_gitignore_file(dir)
        self.open_url()

def update_repo(repo, file = "", content=None, name = None):
    if not content:
        content = read_bytes(file)

    branch = repo.default_branch
    path = name or tail(file)

    try:
        return repo.create_file(
            path=path,
            message=f"uploading {path}",
            content=content,
            branch=branch,
        )

    except Exception as e:
        print(str(e))
        reference = repo.get_contents(path, ref=branch)
        assert(reference)

        return repo.update_file(
            path=reference.path,
            message="Update file content",
            content=content,
            sha=reference.sha,
            branch=branch,
        )



def example(g):
    # g.initialize_local_directory("~/2024") # it wont initialize because it already exists
    g.initialize_local_directory("~/2024-python")
def run(fn, *args, **kwargs):
    controller = GithubController(key='kdog3682')
    with blue_sandwich():
        blue_colon('Howdy', "Starting GithubController")
        blue_colon('Kwargs', kwargs)
        blue_colon('Running the Function', fn)
        blue_colon('Github Instance Initialized', controller)
    fn(controller, *args, **kwargs)

if __name__ == "__main__":
    run(example)
