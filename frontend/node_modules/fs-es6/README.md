# fs-es6
Simple FileSystem API in the browser
> fs-es6 is a module that emulates in-browser the Node JS file system API using the FileSystem API of HTML5. fs-es6 can create, read, navigate, and write in the local file system nicely.

## Installation
```shell
npm install fs-es6
```
Here's a  using the LocalStorage-backed file system:


## Usage
The following is an example of simple use that creates a `canisLupus` folder in the `/tmp` path.

```js
import fs from 'fs-es6'

fs.mkdirSync('/tmp/canisLupus').then()
```

## Override the `fs` module
You can map your project to use this module in place of the standard Node.js fs
module by adding a _browser_ object like so into the package.json before
running the browserify command. Just make sure fs-es6 is installed as a
dependency first.

```json
"browser": {
  "fs": "fs-es6"
}
```

For more info check out the
[Browserify Handbook](https://github.com/substack/browserify-handbook).

## API
fs-es6 has the same interface and many functions like the [standard Node.js API](http://nodejs.org/api/fs.html).

#### fs.createWriteStream(path, options)
Returns a new WriteStream object.

#### fs.writeFile(file, data, callback)
Asynchronously writes data to a file, replacing the file if it already exists. data should be a string.

#### fs.writeFileSync(file, data)
The synchronous version of fs.writeFile().

#### fs.appendFile(file, data, callback)
Asynchronously append data to a file, creating the file if it does not yet exist. data should be a string.

#### fs.appendFileSync(file, data)
The synchronous version of fs.appendFile().

#### fs.readFile(file, callback)
Asynchronously reads the entire contents of a file.

#### fs.readFileSync(file)
Synchronous version of fs.readFile().

#### fs.unlink(path, callback)
Asynchronous delete a file.

#### fs.unlinkSync(path)
Synchronous version of fs.unlinkSync().

#### fs.readdir(path, callback)
Asynchronous reads the contents of a directory.

#### fs.readdirSync(path)
Synchronous version of fs.readdir().

#### fs.mkdir(path, callback)
Asynchronous create a directory.

#### fs.mkdirSync(path)
Synchronous version of fs.mkdir().

#### fs.rmdir(path, callback)
Asynchronous delete a directory. It must be empty.

#### fs.rmdirSync(path)
Synchronous version of fs.rmdir().

#### fs.exists(path, callback) `deprecated`
Test whether or not the given path exists by checking with the file system. Then call the `callback` argument with either true or false.

#### fs.existsSync(path) `deprecated`
Synchronous version of fs.exists().

#### fs.access(path, callback)
Tests a user's permissions for the file or directory specified by `path`

#### fs.accessSync(path)
Synchronous version of fs.access().

#### fs.stat(path, callback)
Get metadata related to a file or directory.

#### fs.statSync(path
Synchronous version of fs.stat().