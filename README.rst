====
Emma
====

Whether you're keeping a journal or writing as a meditation, it's the same
thing. What's important is you're having a relationship with your mind.
-- Natalie Goldberg


Setup
=====

1. $ git clone git@github.com:grantjenks/emma.git
2. $ cd emma
3. $ python3 -m venv --copies env
4. $ source env/bin/activate
5. $ pip install -e .
6. $ emma load
7. System Preferences > Security & Privacy > Screen Recording and allow "python"
8. System Preferences > Security & Privacy > Full Disk Access and allow "python"
9. $ emma reload


Ideas
=====

- Use pynput for keyboard and mouse events
- Add command to gc contents dir based on symlinks
- Make ContentAddressableStorage._save robust to multiple threads/processes
- Move recorder to separate process in status bar to avoid skew
