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
6. System Preferences > Security & Privacy > Screen Recording
   Allow "python" in the virtual env.
7. $ emma load


Ideas
=====

- Use pynput for keyboard and mouse events
- Add command to gc contents dir based on symlinks
- Make ContentAddressableStorage._save robust to multiple threads/processes
- Use multiple processes for Emma:
  1. Status bar process
  2. Recorder process
  3. Server process
  The "Emma" process joins the "Status bar" process, then terminates the
  Recorder and Server process when it exits.
