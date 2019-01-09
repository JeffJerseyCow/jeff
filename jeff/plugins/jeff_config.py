from jeff.core import updateConfig, removeContainer

def parser(subparsers):
    group = subparsers.add_parser('config')
    configParser = group.add_mutually_exclusive_group()
    configParser.add_argument('--show', action='store_true', help='show configuration')
    configParser.add_argument('--list', action='store_true', help='show configuration')
    configParser.add_argument('--rm', type=str, help='delete container')
    configParser.add_argument('--base-domain', type=str, help='change base domain')
    configParser.add_argument('--reset-base-domain', action='store_true', help='reset base domain')

def run(args, config):
    if args.show:
        print(config)
        return True

    elif args.list:
        for container in config['containers']:
            print(container)
        return True

    elif args.rm:
        if removeContainer(args.rm, config):
            print('Deleted "%s"' % args.rm)
            return True
        else:
            print('Error: Container "%s" does not exist' % args.rm)
            return False

    elif args.base_domain:
        config['baseDomain'] = args.base_domain
        updateConfig(config)
        print('Changed base domain to "%s"' % args.base_domain)
        return True

    elif args.reset_base_domain:
        config['baseDomain'] = ""
        updateConfig(config)
        print('Reset base domain')
        return True
