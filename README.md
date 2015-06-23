Chat Parser
====
Chat Parser is a utility to parse chat messages and find special content such
as @mentions, emoticons, and links, and serializes that content to JSON and
other formats.

    "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016"

    {
      "mentions": [
        "bob",
        "john"
      ],
      "emoticons": [
        "success"
      ],
      "links": [
        {
          "url": "https://twitter.com/jdorfman/status/430511497475670016",
          "title": "Twitter / jdorfman: nice @littlebigdetail from ..."
        }
      ]
    }


Installation
====
    $ apt-get install libffi-dev libssl-dev  # requests
    $ apt-get install libxml2-dev libxslt1-dev  # lxml
    $ pip install git+https://github.com/yellottyellott/chat-parser.git

A vagrant file has been included for convenience.

    $ vagrant up
    $ vagrant ssh

    $ echo "@bob, come here real quick" | chatparse
    $ cat examples/mentions.txt | chatparse
    $ cat examples/emoticons.txt | chatparse
    $ cat examples/links.txt | chatparse
    $ cat examples/all.txt | chatparse
    $ cat examples/all.txt | chatparse -v  # For debug logging


Usage
====

    $ echo "Hey, @Finn, check out what @BMO can do: https://www.youtube.com/watch?v=ZRlUmkHlCCg (breadcrumbs)." | chatparse

    {
      "mentions": [
        "bmo",
        "finn"
      ],
      "emoticons": [
        "breadcrumbs"
      ],
      "links": [
        {
          "url": "https://www.youtube.com/watch?v=ZRlUmkHlCCg",
          "title": "Adventure Time   Guardians of Sunshine  song - YouTube"
        }
      ]
    }


Mention Parsing
----
[@mentions][1] are a way to mention a user. Mentions start with an `@` and end
when hitting a non-word character.


    $ echo "@chris you around?" | chatparse

    {
      "mentions": [
        "chris"
      ]
    }


Emoticon Parsing
----
[(emoticons)][2] are alphanumeric strings, no longer than 15 characters,
contained in parenthesis.

    $ echo "Good morning! (megusta) (coffee)" | chatparse

    {
      "emoticons": [
        "megusta",
        "coffee"
      ]
    }


Link Parsing
----
Links are URLs contained in the message, along with the page's title.

    $ echo "Olympics are starting soon; http://www.nbcolympics.com" | chatparse

    {
      "links": [
        {
          "url": "http://www.nbcolympics.com",
          "title": "NBC Olympics | 2014 NBC Olympics in Sochi Russia"
        }
      ]
    }


Development
====

Requirements
----
* [VirtualBox 4.3.28][3]
* [Vagrant 1.7.2][4]


Testing
----

    $ vagrant up
    $ vagrant ssh
    $ py.test --cov-report term-missing --cov chat_parser
    $ py.test -s  # to allow break points

[1]: https://help.hipchat.com/knowledgebase/articles/64429-how-do-mentions-work "HipChat mentions documentatiion"
[2]: https://www.hipchat.com/emoticons "HipChat emoticons documentation"
[3]: https://www.virtualbox.org/ "VirtualBox"
[4]: https://www.vagrantup.com/ "Vagrant"
