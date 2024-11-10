# Plz help me

### Information
⚠️ This is a blue-team challenge. There is no flag but a button that will validate that you patched the vulnerability

- webshell
- The description says that the server will reboot every 10mins

When I read that, I was thinking every 10min? Lets verify
- cron
- systemd timer

By looking at the server I found this `/usr/lib/systemd/system/cleanup.service`
Found also `cleanup.sh` in `/opt`

The script does an `eval` that come from a `GET http://commander:5000`

Using cURL I did query the server and the answer was:
- shutdown -h now

Randomly and some garbage command that was writing decoy file on the disk

By following the `$PATH` I found out another copy of `cleanup.sh` in `/bin` or `/usr/bin` and I had write permission on it
(There is also a comment inside the script telling us to wipe its content and save it)


`vi` or `nano` was not available so

```bash
echo > /bin/cleanup.sh
```
After a couple min the copy in `opt` has been replaced by the empty copy in `/bin`
That was the fix!