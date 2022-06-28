# Commit naming convention

Changes that affect the ***entire*** project:

```sh
$ git commit -m "[Action]: [changes description]"
```


Changes that affect the ***part*** of the project:

```sh
$ git commit -m "[Project part]: [Action]: [changes description]"
```

### Project part

In which part of the project changes were made.

For example: 

>*'Server'*

### Action

The type of changes made to projects since the last commit.

**Types:**

- Add - add something new.
- Refactor - make code readable and maintainable.
- Fix - fix some bug.
- Remove - remove something unnecessary or what needs to be replaced. 
- Update - improve something.

### Changes description

Briefly and clearly describe the changes since the last commit.

## Squashing
If you want to squash several commits, put between names this symbol: *'&'*

For example:

> *'Python client: Fix: ... & Server: Add: ...'*

## Examples

```sh
$ git commit -m "Server: Fix: index view"
```

```sh
$ git commit -m "Python client: Add: group creation"
```

