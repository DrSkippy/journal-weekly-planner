poetry run python bin/nozbe_generator.py -f | poetry run python bin/nozbe_generator.py -s 1 -w -d 2023-03-08 good bad ugly > ./test_files/test1.nozbe.trial
poetry run python bin/nozbe_generator.py -f | poetry run python bin/nozbe_generator.py -s 1 -d 2023-03-08 good bad ugly > ./test_files/test2.nozbe.trial
poetry run python bin/nozbe_generator.py -f | poetry run python bin/nozbe_generator.py -s 2 -w -d 2023-03-08 good bad ugly > ./test_files/test3.nozbe.trial
poetry run python bin/nozbe_generator.py -f | poetry run python bin/nozbe_generator.py -s 1 -w  good bad ugly > ./test_files/test4.nozbe.trial
poetry run python bin/nozbe_generator.py -f | poetry run python bin/nozbe_generator.py  -w  good bad ugly > ./test_files/test5.nozbe.trial

diff ./test_files/test1.nozbe.trial ./test_files/test1.nozbe
diff ./test_files/test2.nozbe.trial ./test_files/test2.nozbe
diff ./test_files/test3.nozbe.trial ./test_files/test3.nozbe
diff ./test_files/test4.nozbe.trial ./test_files/test4.nozbe
diff ./test_files/test5.nozbe.trial ./test_files/test5.nozbe
