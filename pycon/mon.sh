#/bin/bash

watch -n0.5 '
    test -e /run/systemd/transient/mys.service &&
    cat /run/systemd/transient/mys.service && echo ;
    ps axf  | tail -n 15 |grep -v "ps\|tail\|cat\|test\|watch";
    systemctl -q is-active mys.service || systemctl reset-failed;
'
