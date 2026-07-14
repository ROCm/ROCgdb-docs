<head>
  <meta charset="UTF-8">
  <meta name="description" content="Contributing to ROCgdb-docs">
  <meta name="keywords" content="ROCgdb, ROCgdb-docs, contributing, contribute, maintainer, contributor">
</head>

# Contribute to ROCgdb-docs

AMD values and encourages contributions to ROCgdb-docs. If you want to contribute,
first review the following guidance. For general documentation conventions, see
[Contributing to ROCm docs](https://rocm.docs.amd.com/en/latest/contribute/contributing.html).

ROCgdb-docs is the documentation repository for
[ROCgdb](https://github.com/ROCm-Developer-Tools/ROCgdb), the ROCm source-level debugger. This
repository hosts the documentation site and includes the ROCgdb source as a submodule, from which
the base GDB HTML documentation is built.

## Development workflow

ROCgdb-docs uses GitHub to host content, collaborate, and manage version control. We use pull
requests (PRs) for all changes. We use
[GitHub issues](https://github.com/ROCm/ROCgdb-docs/issues) to track known issues, such as errors
or gaps in the documentation.

### Issue tracking

This repository tracks documentation issues only. Report non-documentation issues with ROCgdb
itself at [ROCm/ROCgdb issues](https://github.com/ROCm/ROCgdb/issues).

Before filing a new issue, search the
[existing issues](https://github.com/ROCm/ROCgdb-docs/issues) to make sure your issue isn't
already listed.

General issue guidelines:

* Use your best judgement for issue creation. If your issue is already listed, upvote the issue and
  comment to provide additional details, such as the page affected and how to reproduce the problem.
* If you're not sure whether your issue is the same, err on the side of caution and file your issue.
  You can add a comment that includes the issue number (and link) for the similar issue. If we
  evaluate your issue as being the same as the existing issue, we'll close the duplicate.
* If your issue doesn't exist, use the issue template to file a new issue.
  * When filing an issue, provide as much information as possible, such as the affected page or
    section and a description of the expected and actual content. This helps reduce the time
    required to address your issue.
  * Check your issue regularly, as we may require additional information.

### Pull requests

When you create a pull request, target the **main** branch.

When creating a PR, use the following process.

* Identify the issue you want to fix.
* Target the **main** branch for integration.
* Build the documentation locally and confirm it builds without errors or warnings. See
  [How to build documentation locally](README.md#how-to-build-documentation-locally) for
  instructions.
* Review the rendered HTML output to verify your changes display as intended.
* Check that internal links resolve and code examples are accurate.
* Submit your PR and work with the reviewer or maintainer to get it approved.
* Once approved, the maintainer merges your change and it is included in the next published build.
* We'll inform you once your change is committed.

> [!IMPORTANT]
> By creating a PR, you agree to allow your contribution to be licensed under the
> terms of the LICENSE file in this repository.

You can look up each license on the [ROCm licensing](https://rocm.docs.amd.com/en/latest/about/license.html) page.

### Writing conventions

Match the style and structure of the existing content. ROCgdb-docs follows the
[ROCm documentation conventions](https://rocm.docs.amd.com/en/latest/contribute/contributing.html),
including second-person voice, sentence case headings, and language tags on all code blocks. Prefer
evergreen wording over version-specific details.

## Future development workflow

The current ROCgdb-docs workflow is GitHub-based. If, in the future, we change this platform, the
tools and links may change. In this instance, we will update these contribution guidelines
accordingly.
