from jeff.utils import updateConfig

def parser(subparsers):
    debugParser = subparsers.add_parser('config')
    debugParser.add_argument('--show', action='store_true', help='show configuration')
    debugParser.add_argument('-b', '--base-domain', type=str,
        help='change base domain')
    debugParser.add_argument('--reset-base-domain', action='store_true',
        help='reset base domain')

def run(args, config):
    if args.show:
        print(config)
    elif args.base_domain:
        config['baseDomain'] = args.base_domain
        updateConfig(config)
        print('[*] changed base domain to "%s"' % args.base_domain)
    elif args.reset_base_domain:
        config['baseDomain'] = ""
        updateConfig(config)
        print('[*] reset base domain')

    return True
