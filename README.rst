apk-launcher
============================================================
| Reinstall provided apk -> Start MainActivity -> Logcat(pid of target)

--------------------
How to install
--------------------
.. code:: sh

  $ pip install apk-launcher

or

.. code:: sh

  $ pip install apk-launcher --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"
  
--------------------
How to use
--------------------
.. code:: sh

  $ apk-launcher {YOUR_APK_PATH}

'''''''''''''
Option: no logcat
'''''''''''''
.. code:: sh

  $ apk-launcher {YOUR_APK_PATH} --nolog  
