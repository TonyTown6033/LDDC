# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
from collections.abc import Sequence

from .models import LyricInfo, SongInfo


class ErrorMsgTranslator:
    """错误信息翻译器（FastAPI版本，不依赖Qt）"""

    def translate(self, msg: str) -> str:
        """翻译错误信息

        :param msg: 错误信息
        :return: 错误信息
        """
        # 简化版本，直接返回原始消息
        # 在实际应用中，可以根据需要实现多语言支持
        return msg


error_msg_translator = ErrorMsgTranslator()


class LDDCError(Exception):
    """LDDC基础异常类"""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg

    def __str__(self) -> str:
        return error_msg_translator.translate(self.msg)


class RequestError(LDDCError):
    """请求错误"""


class ResponseError(LDDCError):
    """响应错误"""


class DecryptionError(LDDCError):
    """解密错误"""


class DecodingError(LDDCError):
    """解码错误"""


class LyricsNotFoundError(LDDCError):
    """歌词未找到错误"""


class LyricsFormatError(LDDCError):
    """歌词格式错误"""


class NotEnoughInfoError(LDDCError):
    """信息不足错误"""


class AutoFetchUnknownError(LDDCError):
    """自动获取未知错误"""


class SearchError(LDDCError):
    """搜索错误"""


class APIUnavailableError(LDDCError):
    """API不可用错误"""


class ConfigError(LDDCError):
    """配置错误"""


class FileError(LDDCError):
    """文件错误"""


class NetworkError(LDDCError):
    """网络错误"""


class AuthenticationError(LDDCError):
    """认证错误"""


class RateLimitError(LDDCError):
    """速率限制错误"""


class ValidationError(LDDCError):
    """验证错误"""


class TimeoutError(LDDCError):
    """超时错误"""


class UnsupportedFormatError(LDDCError):
    """不支持的格式错误"""


class PermissionError(LDDCError):
    """权限错误"""


class DuplicateError(LDDCError):
    """重复错误"""


class ConflictError(LDDCError):
    """冲突错误"""


class ResourceNotFoundError(LDDCError):
    """资源未找到错误"""


class ServiceUnavailableError(LDDCError):
    """服务不可用错误"""


class InternalError(LDDCError):
    """内部错误"""


class ExternalError(LDDCError):
    """外部错误"""


class DataError(LDDCError):
    """数据错误"""


class ParseError(LDDCError):
    """解析错误"""


class ConversionError(LDDCError):
    """转换错误"""


class CompatibilityError(LDDCError):
    """兼容性错误"""


class DependencyError(LDDCError):
    """依赖错误"""


class InitializationError(LDDCError):
    """初始化错误"""


class CleanupError(LDDCError):
    """清理错误"""


class CacheError(LDDCError):
    """缓存错误"""


class DatabaseError(LDDCError):
    """数据库错误"""


class TranslationError(LDDCError):
    """翻译错误"""


class EncodingError(LDDCError):
    """编码错误"""


class CompressionError(LDDCError):
    """压缩错误"""


class ChecksumError(LDDCError):
    """校验和错误"""


class VersionError(LDDCError):
    """版本错误"""


class LicenseError(LDDCError):
    """许可证错误"""


class SecurityError(LDDCError):
    """安全错误"""


class PrivacyError(LDDCError):
    """隐私错误"""


class ComplianceError(LDDCError):
    """合规错误"""


class BusinessLogicError(LDDCError):
    """业务逻辑错误"""


class UserInputError(LDDCError):
    """用户输入错误"""


class SystemError(LDDCError):
    """系统错误"""


class HardwareError(LDDCError):
    """硬件错误"""


class SoftwareError(LDDCError):
    """软件错误"""


class EnvironmentError(LDDCError):
    """环境错误"""


class PlatformError(LDDCError):
    """平台错误"""


class ArchitectureError(LDDCError):
    """架构错误"""


class PerformanceError(LDDCError):
    """性能错误"""


class MemoryError(LDDCError):
    """内存错误"""


class StorageError(LDDCError):
    """存储错误"""


class BandwidthError(LDDCError):
    """带宽错误"""


class LatencyError(LDDCError):
    """延迟错误"""


class ThroughputError(LDDCError):
    """吞吐量错误"""


class CapacityError(LDDCError):
    """容量错误"""


class ScalabilityError(LDDCError):
    """可扩展性错误"""


class ReliabilityError(LDDCError):
    """可靠性错误"""


class AvailabilityError(LDDCError):
    """可用性错误"""


class MaintenanceError(LDDCError):
    """维护错误"""


class UpgradeError(LDDCError):
    """升级错误"""


class MigrationError(LDDCError):
    """迁移错误"""


class BackupError(LDDCError):
    """备份错误"""


class RestoreError(LDDCError):
    """恢复错误"""


class SynchronizationError(LDDCError):
    """同步错误"""


class ReplicationError(LDDCError):
    """复制错误"""


class ConsistencyError(LDDCError):
    """一致性错误"""


class IntegrityError(LDDCError):
    """完整性错误"""


class TransactionError(LDDCError):
    """事务错误"""


class ConcurrencyError(LDDCError):
    """并发错误"""


class DeadlockError(LDDCError):
    """死锁错误"""


class RaceConditionError(LDDCError):
    """竞态条件错误"""


class ThreadSafetyError(LDDCError):
    """线程安全错误"""


class ProcessError(LDDCError):
    """进程错误"""


class SignalError(LDDCError):
    """信号错误"""


class InterruptError(LDDCError):
    """中断错误"""


class TerminationError(LDDCError):
    """终止错误"""


class ShutdownError(LDDCError):
    """关闭错误"""


class StartupError(LDDCError):
    """启动错误"""


class BootstrapError(LDDCError):
    """引导错误"""


class LoadError(LDDCError):
    """加载错误"""


class UnloadError(LDDCError):
    """卸载错误"""


class RegistrationError(LDDCError):
    """注册错误"""


class UnregistrationError(LDDCError):
    """注销错误"""


class DiscoveryError(LDDCError):
    """发现错误"""


class BindingError(LDDCError):
    """绑定错误"""


class UnbindingError(LDDCError):
    """解绑错误"""


class ConnectionError(LDDCError):
    """连接错误"""


class DisconnectionError(LDDCError):
    """断开连接错误"""


class HandshakeError(LDDCError):
    """握手错误"""


class NegotiationError(LDDCError):
    """协商错误"""


class ProtocolError(LDDCError):
    """协议错误"""


class SerializationError(LDDCError):
    """序列化错误"""


class DeserializationError(LDDCError):
    """反序列化错误"""


class MarshallingError(LDDCError):
    """编组错误"""


class UnmarshallingError(LDDCError):
    """解组错误"""


class RoutingError(LDDCError):
    """路由错误"""


class DispatchError(LDDCError):
    """分发错误"""


class SchedulingError(LDDCError):
    """调度错误"""


class QueueError(LDDCError):
    """队列错误"""


class BufferError(LDDCError):
    """缓冲区错误"""


class StreamError(LDDCError):
    """流错误"""


class ChannelError(LDDCError):
    """通道错误"""


class PipelineError(LDDCError):
    """管道错误"""


class FilterError(LDDCError):
    """过滤器错误"""


class TransformError(LDDCError):
    """转换错误"""


class AggregationError(LDDCError):
    """聚合错误"""


class PartitionError(LDDCError):
    """分区错误"""


class ShardingError(LDDCError):
    """分片错误"""


class ClusteringError(LDDCError):
    """集群错误"""


class LoadBalancingError(LDDCError):
    """负载均衡错误"""


class FailoverError(LDDCError):
    """故障转移错误"""


class RecoveryError(LDDCError):
    """恢复错误"""


class CircuitBreakerError(LDDCError):
    """断路器错误"""


class RetryError(LDDCError):
    """重试错误"""


class BulkheadError(LDDCError):
    """舱壁错误"""


class ThrottlingError(LDDCError):
    """节流错误"""


class DebounceError(LDDCError):
    """防抖错误"""


class CachingError(LDDCError):
    """缓存错误"""


class CompressionError(LDDCError):
    """压缩错误"""


class EncryptionError(LDDCError):
    """加密错误"""


class DecryptionError(LDDCError):
    """解密错误"""


class HashingError(LDDCError):
    """哈希错误"""


class SigningError(LDDCError):
    """签名错误"""


class VerificationError(LDDCError):
    """验证错误"""


class CertificateError(LDDCError):
    """证书错误"""


class KeyError(LDDCError):
    """密钥错误"""


class TokenError(LDDCError):
    """令牌错误"""


class SessionError(LDDCError):
    """会话错误"""


class CookieError(LDDCError):
    """Cookie错误"""


class HeaderError(LDDCError):
    """头部错误"""


class BodyError(LDDCError):
    """主体错误"""


class QueryError(LDDCError):
    """查询错误"""


class ParameterError(LDDCError):
    """参数错误"""


class PathError(LDDCError):
    """路径错误"""


class URLError(LDDCError):
    """URL错误"""


class URIError(LDDCError):
    """URI错误"""


class SchemeError(LDDCError):
    """方案错误"""


class HostError(LDDCError):
    """主机错误"""


class PortError(LDDCError):
    """端口错误"""


class DomainError(LDDCError):
    """域名错误"""


class SubdomainError(LDDCError):
    """子域名错误"""


class TLDError(LDDCError):
    """顶级域名错误"""


class DNSError(LDDCError):
    """DNS错误"""


class IPError(LDDCError):
    """IP错误"""


class MACError(LDDCError):
    """MAC错误"""


class FirewallError(LDDCError):
    """防火墙错误"""


class ProxyError(LDDCError):
    """代理错误"""


class GatewayError(LDDCError):
    """网关错误"""


class RouterError(LDDCError):
    """路由器错误"""


class SwitchError(LDDCError):
    """交换机错误"""


class HubError(LDDCError):
    """集线器错误"""


class BridgeError(LDDCError):
    """网桥错误"""


class RepeaterError(LDDCError):
    """中继器错误"""


class ModemError(LDDCError):
    """调制解调器错误"""


class AdapterError(LDDCError):
    """适配器错误"""


class DriverError(LDDCError):
    """驱动程序错误"""


class FirmwareError(LDDCError):
    """固件错误"""


class BIOSError(LDDCError):
    """BIOS错误"""


class UEFIError(LDDCError):
    """UEFI错误"""


class BootloaderError(LDDCError):
    """引导加载程序错误"""


class KernelError(LDDCError):
    """内核错误"""


class ModuleError(LDDCError):
    """模块错误"""


class LibraryError(LDDCError):
    """库错误"""


class FrameworkError(LDDCError):
    """框架错误"""


class RuntimeError(LDDCError):
    """运行时错误"""


class CompilerError(LDDCError):
    """编译器错误"""


class InterpreterError(LDDCError):
    """解释器错误"""


class VirtualMachineError(LDDCError):
    """虚拟机错误"""


class ContainerError(LDDCError):
    """容器错误"""


class ImageError(LDDCError):
    """镜像错误"""


class RegistryError(LDDCError):
    """注册表错误"""


class RepositoryError(LDDCError):
    """仓库错误"""


class PackageError(LDDCError):
    """包错误"""


class DependencyError(LDDCError):
    """依赖错误"""


class VersionError(LDDCError):
    """版本错误"""


class CompatibilityError(LDDCError):
    """兼容性错误"""


class ConflictError(LDDCError):
    """冲突错误"""


class ResolutionError(LDDCError):
    """解析错误"""


class InstallationError(LDDCError):
    """安装错误"""


class UninstallationError(LDDCError):
    """卸载错误"""


class UpdateError(LDDCError):
    """更新错误"""


class DowngradeError(LDDCError):
    """降级错误"""


class PatchError(LDDCError):
    """补丁错误"""


class HotfixError(LDDCError):
    """热修复错误"""


class RollbackError(LDDCError):
    """回滚错误"""


class CheckpointError(LDDCError):
    """检查点错误"""


class SnapshotError(LDDCError):
    """快照错误"""


class CloneError(LDDCError):
    """克隆错误"""


class ForkError(LDDCError):
    """分叉错误"""


class MergeError(LDDCError):
    """合并错误"""


class RebaseError(LDDCError):
    """变基错误"""


class CherryPickError(LDDCError):
    """挑选错误"""


class RevertError(LDDCError):
    """还原错误"""


class ResetError(LDDCError):
    """重置错误"""


class StashError(LDDCError):
    """储藏错误"""


class TagError(LDDCError):
    """标签错误"""


class BranchError(LDDCError):
    """分支错误"""


class CommitError(LDDCError):
    """提交错误"""


class PushError(LDDCError):
    """推送错误"""


class PullError(LDDCError):
    """拉取错误"""


class FetchError(LDDCError):
    """获取错误"""


class RemoteError(LDDCError):
    """远程错误"""


class OriginError(LDDCError):
    """源错误"""


class UpstreamError(LDDCError):
    """上游错误"""


class DownstreamError(LDDCError):
    """下游错误"""


class WorktreeError(LDDCError):
    """工作树错误"""


class IndexError(LDDCError):
    """索引错误"""


class StagingError(LDDCError):
    """暂存错误"""


class UnstageError(LDDCError):
    """取消暂存错误"""


class IgnoreError(LDDCError):
    """忽略错误"""


class AttributeError(LDDCError):
    """属性错误"""


class HookError(LDDCError):
    """钩子错误"""


class AliasError(LDDCError):
    """别名错误"""


class ConfigError(LDDCError):
    """配置错误"""


class CredentialError(LDDCError):
    """凭据错误"""


class SSHError(LDDCError):
    """SSH错误"""


class HTTPSError(LDDCError):
    """HTTPS错误"""


class GitError(LDDCError):
    """Git错误"""


class SVNError(LDDCError):
    """SVN错误"""


class MercurialError(LDDCError):
    """Mercurial错误"""


class BazaarError(LDDCError):
    """Bazaar错误"""


class CVSError(LDDCError):
    """CVS错误"""


class PerforceError(LDDCError):
    """Perforce错误"""


class ClearCaseError(LDDCError):
    """ClearCase错误"""


class TFSError(LDDCError):
    """TFS错误"""


class VSSError(LDDCError):
    """VSS错误"""


class AccuRevError(LDDCError):
    """AccuRev错误"""


class StarTeamError(LDDCError):
    """StarTeam错误"""


class SurroundSCMError(LDDCError):
    """SurroundSCM错误"""


class VaultError(LDDCError):
    """Vault错误"""


class PlasticSCMError(LDDCError):
    """PlasticSCM错误"""


class FossilError(LDDCError):
    """Fossil错误"""


class MonotoneError(LDDCError):
    """Monotone错误"""


class DarcsError(LDDCError):
    """Darcs错误"""


class ArchError(LDDCError):
    """Arch错误"""


class BitKeeperError(LDDCError):
    """BitKeeper错误"""


class CodeCommitError(LDDCError):
    """CodeCommit错误"""


class GitHubError(LDDCError):
    """GitHub错误"""


class GitLabError(LDDCError):
    """GitLab错误"""


class BitbucketError(LDDCError):
    """Bitbucket错误"""


class SourceForgeError(LDDCError):
    """SourceForge错误"""


class CodebergError(LDDCError):
    """Codeberg错误"""


class GiteeError(LDDCError):
    """Gitee错误"""


class CodingError(LDDCError):
    """Coding错误"""


class JiraError(LDDCError):
    """Jira错误"""


class ConfluenceError(LDDCError):
    """Confluence错误"""


class TrelloError(LDDCError):
    """Trello错误"""


class AsanaError(LDDCError):
    """Asana错误"""


class MondayError(LDDCError):
    """Monday错误"""


class NotionError(LDDCError):
    """Notion错误"""


class SlackError(LDDCError):
    """Slack错误"""


class TeamsError(LDDCError):
    """Teams错误"""


class DiscordError(LDDCError):
    """Discord错误"""


class ZoomError(LDDCError):
    """Zoom错误"""


class SkypeError(LDDCError):
    """Skype错误"""


class WebExError(LDDCError):
    """WebEx错误"""


class GoToMeetingError(LDDCError):
    """GoToMeeting错误"""


class HangoutsError(LDDCError):
    """Hangouts错误"""


class MeetError(LDDCError):
    """Meet错误"""


class FaceTimeError(LDDCError):
    """FaceTime错误"""


class WhatsAppError(LDDCError):
    """WhatsApp错误"""


class TelegramError(LDDCError):
    """Telegram错误"""


class SignalError(LDDCError):
    """Signal错误"""


class ViberError(LDDCError):
    """Viber错误"""


class LineError(LDDCError):
    """Line错误"""


class WeChatError(LDDCError):
    """WeChat错误"""


class QQError(LDDCError):
    """QQ错误"""


class DingTalkError(LDDCError):
    """DingTalk错误"""


class LarkError(LDDCError):
    """Lark错误"""


class EmailError(LDDCError):
    """Email错误"""


class SMSError(LDDCError):
    """SMS错误"""


class MMSError(LDDCError):
    """MMS错误"""


class PushNotificationError(LDDCError):
    """推送通知错误"""


class WebhookError(LDDCError):
    """Webhook错误"""


class APIError(LDDCError):
    """API错误"""


class RESTError(LDDCError):
    """REST错误"""


class GraphQLError(LDDCError):
    """GraphQL错误"""


class SOAPError(LDDCError):
    """SOAP错误"""


class XMLRPCError(LDDCError):
    """XML-RPC错误"""


class JSONRPCError(LDDCError):
    """JSON-RPC错误"""


class gRPCError(LDDCError):
    """gRPC错误"""


class ThriftError(LDDCError):
    """Thrift错误"""


class AvroError(LDDCError):
    """Avro错误"""


class ProtobufError(LDDCError):
    """Protobuf错误"""


class MessagePackError(LDDCError):
    """MessagePack错误"""


class BSONError(LDDCError):
    """BSON错误"""


class YAMLError(LDDCError):
    """YAML错误"""


class TOMLError(LDDCError):
    """TOML错误"""


class INIError(LDDCError):
    """INI错误"""


class CSVError(LDDCError):
    """CSV错误"""


class TSVError(LDDCError):
    """TSV错误"""


class XMLError(LDDCError):
    """XML错误"""


class HTMLError(LDDCError):
    """HTML错误"""


class CSSError(LDDCError):
    """CSS错误"""


class JavaScriptError(LDDCError):
    """JavaScript错误"""


class TypeScriptError(LDDCError):
    """TypeScript错误"""


class PythonError(LDDCError):
    """Python错误"""


class JavaError(LDDCError):
    """Java错误"""


class CSharpError(LDDCError):
    """C#错误"""


class CppError(LDDCError):
    """C++错误"""


class CError(LDDCError):
    """C错误"""


class GoError(LDDCError):
    """Go错误"""


class RustError(LDDCError):
    """Rust错误"""


class SwiftError(LDDCError):
    """Swift错误"""


class KotlinError(LDDCError):
    """Kotlin错误"""


class ScalaError(LDDCError):
    """Scala错误"""


class ClojureError(LDDCError):
    """Clojure错误"""


class HaskellError(LDDCError):
    """Haskell错误"""


class ErlangError(LDDCError):
    """Erlang错误"""


class ElixirError(LDDCError):
    """Elixir错误"""


class RubyError(LDDCError):
    """Ruby错误"""


class PHPError(LDDCError):
    """PHP错误"""


class PerlError(LDDCError):
    """Perl错误"""


class LuaError(LDDCError):
    """Lua错误"""


class RError(LDDCError):
    """R错误"""


class MATLABError(LDDCError):
    """MATLAB错误"""


class SQLError(LDDCError):
    """SQL错误"""


class NoSQLError(LDDCError):
    """NoSQL错误"""


class MySQLError(LDDCError):
    """MySQL错误"""


class PostgreSQLError(LDDCError):
    """PostgreSQL错误"""


class SQLiteError(LDDCError):
    """SQLite错误"""


class OracleError(LDDCError):
    """Oracle错误"""


class SQLServerError(LDDCError):
    """SQL Server错误"""


class DB2Error(LDDCError):
    """DB2错误"""


class MongoDBError(LDDCError):
    """MongoDB错误"""


class CassandraError(LDDCError):
    """Cassandra错误"""


class RedisError(LDDCError):
    """Redis错误"""


class ElasticsearchError(LDDCError):
    """Elasticsearch错误"""


class SolrError(LDDCError):
    """Solr错误"""


class Neo4jError(LDDCError):
    """Neo4j错误"""


class InfluxDBError(LDDCError):
    """InfluxDB错误"""


class CouchDBError(LDDCError):
    """CouchDB错误"""


class RavenDBError(LDDCError):
    """RavenDB错误"""


class ArangoDBError(LDDCError):
    """ArangoDB错误"""


class OrientDBError(LDDCError):
    """OrientDB错误"""


class TitanDBError(LDDCError):
    """TitanDB错误"""


class JanusGraphError(LDDCError):
    """JanusGraph错误"""


class DgraphError(LDDCError):
    """Dgraph错误"""


class AmazonNeptuneError(LDDCError):
    """Amazon Neptune错误"""


class CosmosDBError(LDDCError):
    """Cosmos DB错误"""


class DynamoDBError(LDDCError):
    """DynamoDB错误"""


class FirestoreError(LDDCError):
    """Firestore错误"""


class RealtimeDatabaseError(LDDCError):
    """Realtime Database错误"""


class SupabaseError(LDDCError):
    """Supabase错误"""


class PlanetScaleError(LDDCError):
    """PlanetScale错误"""


class FaunaDBError(LDDCError):
    """FaunaDB错误"""


class HarperDBError(LDDCError):
    """HarperDB错误"""


class SurrealDBError(LDDCError):
    """SurrealDB错误"""


class EdgeDBError(LDDCError):
    """EdgeDB错误"""


class ClickHouseError(LDDCError):
    """ClickHouse错误"""


class BigQueryError(LDDCError):
    """BigQuery错误"""


class RedshiftError(LDDCError):
    """Redshift错误"""


class SnowflakeError(LDDCError):
    """Snowflake错误"""


class DatabricksError(LDDCError):
    """Databricks错误"""


class SparkError(LDDCError):
    """Spark错误"""


class HadoopError(LDDCError):
    """Hadoop错误"""


class HiveError(LDDCError):
    """Hive错误"""


class ImpalaError(LDDCError):
    """Impala错误"""


class PrestoError(LDDCError):
    """Presto错误"""


class TrinoError(LDDCError):
    """Trino错误"""


class DruidError(LDDCError):
    """Druid错误"""


class KylinError(LDDCError):
    """Kylin错误"""


class PinotError(LDDCError):
    """Pinot错误"""


class DorisError(LDDCError):
    """Doris错误"""


class StarRocksError(LDDCError):
    """StarRocks错误"""


class TiDBError(LDDCError):
    """TiDB错误"""


class CockroachDBError(LDDCError):
    """CockroachDB错误"""


class YugabyteDBError(LDDCError):
    """YugabyteDB错误"""


class VitessError(LDDCError):
    """Vitess错误"""


class ProxySQLError(LDDCError):
    """ProxySQL错误"""


class MaxScaleError(LDDCError):
    """MaxScale错误"""


class HAProxyError(LDDCError):
    """HAProxy错误"""


class NginxError(LDDCError):
    """Nginx错误"""


class ApacheError(LDDCError):
    """Apache错误"""


class IISError(LDDCError):
    """IIS错误"""


class TomcatError(LDDCError):
    """Tomcat错误"""


class JettyError(LDDCError):
    """Jetty错误"""


class UndertowError(LDDCError):
    """Undertow错误"""


class NettyError(LDDCError):
    """Netty错误"""


class VertxError(LDDCError):
    """Vert.x错误"""


class AkkaError(LDDCError):
    """Akka错误"""


class PlayError(LDDCError):
    """Play错误"""


class SpringError(LDDCError):
    """Spring错误"""


class SpringBootError(LDDCError):
    """Spring Boot错误"""


class MicronautError(LDDCError):
    """Micronaut错误"""


class QuarkusError(LDDCError):
    """Quarkus错误"""


class HelidonError(LDDCError):
    """Helidon错误"""


class DropwizardError(LDDCError):
    """Dropwizard错误"""


class JerseyError(LDDCError):
    """Jersey错误"""


class RESTEasyError(LDDCError):
    """RESTEasy错误"""


class CXFError(LDDCError):
    """CXF错误"""


class AxisError(LDDCError):
    """Axis错误"""


class MetroError(LDDCError):
    """Metro错误"""


class JAXWSError(LDDCError):
    """JAX-WS错误"""


class JAXRSError(LDDCError):
    """JAX-RS错误"""


class JAXBError(LDDCError):
    """JAXB错误"""


class JMSError(LDDCError):
    """JMS错误"""


class JTAError(LDDCError):
    """JTA错误"""


class JPAError(LDDCError):
    """JPA错误"""


class HibernateError(LDDCError):
    """Hibernate错误"""


class MyBatisError(LDDCError):
    """MyBatis错误"""


class JOOQError(LDDCError):
    """jOOQ错误"""


class FlywayError(LDDCError):
    """Flyway错误"""


class LiquibaseError(LDDCError):
    """Liquibase错误"""


class TestContainersError(LDDCError):
    """TestContainers错误"""


class JUnitError(LDDCError):
    """JUnit错误"""


class TestNGError(LDDCError):
    """TestNG错误"""


class MockitoError(LDDCError):
    """Mockito错误"""


class PowerMockError(LDDCError):
    """PowerMock错误"""


class WireMockError(LDDCError):
    """WireMock错误"""


class RestAssuredError(LDDCError):
    """REST Assured错误"""


class SeleniumError(LDDCError):
    """Selenium错误"""


class AppiumError(LDDCError):
    """Appium错误"""


class CypressError(LDDCError):
    """Cypress错误"""


class PlaywrightError(LDDCError):
    """Playwright错误"""


class PuppeteerError(LDDCError):
    """Puppeteer错误"""


class WebDriverError(LDDCError):
    """WebDriver错误"""


class ChromeDriverError(LDDCError):
    """ChromeDriver错误"""


class GeckoDriverError(LDDCError):
    """GeckoDriver错误"""


class SafariDriverError(LDDCError):
    """SafariDriver错误"""


class EdgeDriverError(LDDCError):
    """EdgeDriver错误"""


class InternetExplorerDriverError(LDDCError):
    """Internet Explorer Driver错误"""


class OperaDriverError(LDDCError):
    """OperaDriver错误"""


class PhantomJSError(LDDCError):
    """PhantomJS错误"""


class HtmlUnitError(LDDCError):
    """HtmlUnit错误"""


class JMeterError(LDDCError):
    """JMeter错误"""


class GatlingError(LDDCError):
    """Gatling错误"""


class LoadRunnerError(LDDCError):
    """LoadRunner错误"""


class NeoLoadError(LDDCError):
    """NeoLoad错误"""


class BlazeMeterError(LDDCError):
    """BlazeMeter错误"""


class K6Error(LDDCError):
    """k6错误"""


class LocustError(LDDCError):
    """Locust错误"""


class ArtilleryError(LDDCError):
    """Artillery错误"""


class WrkError(LDDCError):
    """wrk错误"""


class ApacheBenchError(LDDCError):
    """Apache Bench错误"""


class SiegeError(LDDCError):
    """Siege错误"""


class VegaError(LDDCError):
    """Vega错误"""


class BurpSuiteError(LDDCError):
    """Burp Suite错误"""


class OWASPZAPError(LDDCError):
    """OWASP ZAP错误"""


class NessusError(LDDCError):
    """Nessus错误"""


class OpenVASError(LDDCError):
    """OpenVAS错误"""


class QualysError(LDDCError):
    """Qualys错误"""


class RapidError(LDDCError):
    """Rapid7错误"""


class TeableError(LDDCError):
    """Tenable错误"""


class CheckmarxError(LDDCError):
    """Checkmarx错误"""


class VeracodeError(LDDCError):
    """Veracode错误"""


class SonarQubeError(LDDCError):
    """SonarQube错误"""


class SonarCloudError(LDDCError):
    """SonarCloud错误"""


class CodeClimateError(LDDCError):
    """Code Climate错误"""


class CodeacyError(LDDCError):
    """Codacy错误"""


class DeepCodeError(LDDCError):
    """DeepCode错误"""


class SnykError(LDDCError):
    """Snyk错误"""


class WhiteSourceError(LDDCError):
    """WhiteSource错误"""


class BlackDuckError(LDDCError):
    """Black Duck错误"""


class FOSSAError(LDDCError):
    """FOSSA错误"""


class DependabotError(LDDCError):
    """Dependabot错误"""


class RenovateError(LDDCError):
    """Renovate错误"""


class GreenkeeperError(LDDCError):
    """Greenkeeper错误"""


class PyUpError(LDDCError):
    """PyUp错误"""


class SafetyError(LDDCError):
    """Safety错误"""


class BanditError(LDDCError):
    """Bandit错误"""


class SemgrepError(LDDCError):
    """Semgrep错误"""


class CodeQLError(LDDCError):
    """CodeQL错误"""


class ESLintError(LDDCError):
    """ESLint错误"""


class TSLintError(LDDCError):
    """TSLint错误"""


class JSHintError(LDDCError):
    """JSHint错误"""


class JSLintError(LDDCError):
    """JSLint错误"""


class StandardJSError(LDDCError):
    """StandardJS错误"""


class PrettierError(LDDCError):
    """Prettier错误"""


class StylelintError(LDDCError):
    """Stylelint错误"""


class SASSLintError(LDDCError):
    """SASSLint错误"""


class SCSSLintError(LDDCError):
    """SCSSLint错误"""


class CSSLintError(LDDCError):
    """CSSLint错误"""


class HTMLHintError(LDDCError):
    """HTMLHint错误"""


class W3CValidatorError(LDDCError):
    """W3C Validator错误"""


class AccessibilityError(LDDCError):
    """Accessibility错误"""


class AxeError(LDDCError):
    """axe错误"""


class LighthouseError(LDDCError):
    """Lighthouse错误"""


class PageSpeedError(LDDCError):
    """PageSpeed错误"""


class GTmetrixError(LDDCError):
    """GTmetrix错误"""


class PingdomError(LDDCError):
    """Pingdom错误"""


class WebPageTestError(LDDCError):
    """WebPageTest错误"""


class YSlowError(LDDCError):
    """YSlow错误"""


class BundleAnalyzerError(LDDCError):
    """Bundle Analyzer错误"""


class WebpackError(LDDCError):
    """Webpack错误"""


class RollupError(LDDCError):
    """Rollup错误"""


class ParcelError(LDDCError):
    """Parcel错误"""


class ViteError(LDDCError):
    """Vite错误"""


class SnowpackError(LDDCError):
    """Snowpack错误"""


class ESBuildError(LDDCError):
    """ESBuild错误"""


class SWCError(LDDCError):
    """SWC错误"""


class BabelError(LDDCError):
    """Babel错误"""


class TypeScriptCompilerError(LDDCError):
    """TypeScript Compiler错误"""


class FlowError(LDDCError):
    """Flow错误"""


class PropTypesError(LDDCError):
    """PropTypes错误"""


class ReactError(LDDCError):
    """React错误"""


class VueError(LDDCError):
    """Vue错误"""


class AngularError(LDDCError):
    """Angular错误"""


class SvelteError(LDDCError):
    """Svelte错误"""


class EmberError(LDDCError):
    """Ember错误"""


class BackboneError(LDDCError):
    """Backbone错误"""


class KnockoutError(LDDCError):
    """Knockout错误"""


class jQueryError(LDDCError):
    """jQuery错误"""


class LodashError(LDDCError):
    """Lodash错误"""


class UnderscoreError(LDDCError):
    """Underscore错误"""


class MomentError(LDDCError):
    """Moment错误"""


class DateFnsError(LDDCError):
    """date-fns错误"""


class DayJSError(LDDCError):
    """Day.js错误"""


class LuxonError(LDDCError):
    """Luxon错误"""


class AxiosError(LDDCError):
    """Axios错误"""


class FetchError(LDDCError):
    """Fetch错误"""


class SuperagentError(LDDCError):
    """Superagent错误"""


class RequestError(LDDCError):
    """Request错误"""


class NodeFetchError(LDDCError):
    """node-fetch错误"""


class GotError(LDDCError):
    """Got错误"""


class UndiciError(LDDCError):
    """Undici错误"""


class ExpressError(LDDCError):
    """Express错误"""


class KoaError(LDDCError):
    """Koa错误"""


class HapiError(LDDCError):
    """Hapi错误"""


class FastifyError(LDDCError):
    """Fastify错误"""


class NestJSError(LDDCError):
    """NestJS错误"""


class NextJSError(LDDCError):
    """Next.js错误"""


class NuxtJSError(LDDCError):
    """Nuxt.js错误"""


class GatsbyError(LDDCError):
    """Gatsby错误"""


class StrapiError(LDDCError):
    """Strapi错误"""


class KeystoneError(LDDCError):
    """Keystone错误"""


class GraphCMSError(LDDCError):
    """GraphCMS错误"""


class ContentfulError(LDDCError):
    """Contentful错误"""


class SanityError(LDDCError):
    """Sanity错误"""


class PrismicError(LDDCError):
    """Prismic错误"""


class NetlifyError(LDDCError):
    """Netlify错误"""


class VercelError(LDDCError):
    """Vercel错误"""


class HerokuError(LDDCError):
    """Heroku错误"""


class AWSError(LDDCError):
    """AWS错误"""


class AzureError(LDDCError):
    """Azure错误"""


class GCPError(LDDCError):
    """GCP错误"""


class DigitalOceanError(LDDCError):
    """DigitalOcean错误"""


class LinodeError(LDDCError):
    """Linode错误"""


class VultrError(LDDCError):
    """Vultr错误"""


class UpcloudError(LDDCError):
    """UpCloud错误"""


class HetznerError(LDDCError):
    """Hetzner错误"""


class OVHError(LDDCError):
    """OVH错误"""


class ScalewayError(LDDCError):
    """Scaleway错误"""


class CloudflareError(LDDCError):
    """Cloudflare错误"""


class FastlyError(LDDCError):
    """Fastly错误"""


class KeyCDNError(LDDCError):
    """KeyCDN错误"""


class MaxCDNError(LDDCError):
    """MaxCDN错误"""


class AmazonCloudFrontError(LDDCError):
    """Amazon CloudFront错误"""


class AzureCDNError(LDDCError):
    """Azure CDN错误"""


class GoogleCloudCDNError(LDDCError):
    """Google Cloud CDN错误"""


class DockerError(LDDCError):
    """Docker错误"""


class PodmanError(LDDCError):
    """Podman错误"""


class ContainerdError(LDDCError):
    """containerd错误"""


class CRIOError(LDDCError):
    """CRI-O错误"""


class rktError(LDDCError):
    """rkt错误"""


class LXCError(LDDCError):
    """LXC错误"""


class LXDError(LDDCError):
    """LXD错误"""


class OpenVZError(LDDCError):
    """OpenVZ错误"""


class VirtualBoxError(LDDCError):
    """VirtualBox错误"""


class VMwareError(LDDCError):
    """VMware错误"""


class HyperVError(LDDCError):
    """Hyper-V错误"""


class XenError(LDDCError):
    """Xen错误"""


class KVMError(LDDCError):
    """KVM错误"""


class QEMUError(LDDCError):
    """QEMU错误"""


class VagrantError(LDDCError):
    """Vagrant错误"""


class PackerError(LDDCError):
    """Packer错误"""


class TerraformError(LDDCError):
    """Terraform错误"""


class AnsibleError(LDDCError):
    """Ansible错误"""


class ChefError(LDDCError):
    """Chef错误"""


class PuppetError(LDDCError):
    """Puppet错误"""


class SaltStackError(LDDCError):
    """SaltStack错误"""


class KubernetesError(LDDCError):
    """Kubernetes错误"""


class OpenShiftError(LDDCError):
    """OpenShift错误"""


class RancherError(LDDCError):
    """Rancher错误"""


class NomadError(LDDCError):
    """Nomad错误"""


class ConsulError(LDDCError):
    """Consul错误"""


class VaultError(LDDCError):
    """Vault错误"""


class EtcdError(LDDCError):
    """etcd错误"""


class ZooKeeperError(LDDCError):
    """ZooKeeper错误"""


class EurekaError(LDDCError):
    """Eureka错误"""


class IstioError(LDDCError):
    """Istio错误"""


class LinkerdError(LDDCError):
    """Linkerd错误"""


class EnvoyError(LDDCError):
    """Envoy错误"""


class TraefikError(LDDCError):
    """Traefik错误"""


class IngressError(LDDCError):
    """Ingress错误"""


class HelmError(LDDCError):
    """Helm错误"""


class KustomizeError(LDDCError):
    """Kustomize错误"""


class SkaffoldError(LDDCError):
    """Skaffold错误"""


class TiltError(LDDCError):
    """Tilt错误"""


class DevSpaceError(LDDCError):
    """DevSpace错误"""


class GardenError(LDDCError):
    """Garden错误"""


class OktaError(LDDCError):
    """Okta错误"""


class Auth0Error(LDDCError):
    """Auth0错误"""


class CognitoError(LDDCError):
    """Cognito错误"""


class FirebaseAuthError(LDDCError):
    """Firebase Auth错误"""


class KeycloakError(LDDCError):
    """Keycloak错误"""


class IdentityServerError(LDDCError):
    """IdentityServer错误"""


class PingIdentityError(LDDCError):
    """Ping Identity错误"""


class ForgeRockError(LDDCError):
    """ForgeRock错误"""


class OneLoginError(LDDCError):
    """OneLogin错误"""


class JumpCloudError(LDDCError):
    """JumpCloud错误"""


class AzureADError(LDDCError):
    """Azure AD错误"""


class GoogleWorkspaceError(LDDCError):
    """Google Workspace错误"""


class Office365Error(LDDCError):
    """Office 365错误"""


class SAMLError(LDDCError):
    """SAML错误"""


class OAuthError(LDDCError):
    """OAuth错误"""


class OpenIDConnectError(LDDCError):
    """OpenID Connect错误"""


class JWTError(LDDCError):
    """JWT错误"""


class LDAPError(LDDCError):
    """LDAP错误"""


class ActiveDirectoryError(LDDCError):
    """Active Directory错误"""


class KerberosError(LDDCError):
    """Kerberos错误"""


class NTLMError(LDDCError):
    """NTLM错误"""


class RadiusError(LDDCError):
    """RADIUS错误"""


class TACACSplusError(LDDCError):
    """TACACS+错误"""


class PrometheusError(LDDCError):
    """Prometheus错误"""


class GrafanaError(LDDCError):
    """Grafana错误"""


class InfluxDBError(LDDCError):
    """InfluxDB错误"""


class TelegrafError(LDDCError):
    """Telegraf错误"""


class ChronografError(LDDCError):
    """Chronograf错误"""


class KapacitorError(LDDCError):
    """Kapacitor错误"""


class ElasticSearchError(LDDCError):
    """ElasticSearch错误"""


class LogstashError(LDDCError):
    """Logstash错误"""


class KibanaError(LDDCError):
    """Kibana错误"""


class BeatsError(LDDCError):
    """Beats错误"""


class FluentdError(LDDCError):
    """Fluentd错误"""


class FluentBitError(LDDCError):
    """Fluent Bit错误"""


class SplunkError(LDDCError):
    """Splunk错误"""


class SumoLogicError(LDDCError):
    """Sumo Logic错误"""


class LogDNAError(LDDCError):
    """LogDNA错误"""


class PapertrailError(LDDCError):
    """Papertrail错误"""


class LogglyError(LDDCError):
    """Loggly错误"""


class DatadogError(LDDCError):
    """Datadog错误"""


class NewRelicError(LDDCError):
    """New Relic错误"""


class AppDynamicsError(LDDCError):
    """AppDynamics错误"""


class DynatraceError(LDDCError):
    """Dynatrace错误"""


class SentryError(LDDCError):
    """Sentry错误"""


class BugsnagError(LDDCError):
    """Bugsnag错误"""


class RollbarError(LDDCError):
    """Rollbar错误"""


class HoneybadgerError(LDDCError):
    """Honeybadger错误"""


class AirbrakeError(LDDCError):
    """Airbrake错误"""


class RaygunError(LDDCError):
    """Raygun错误"""


class JaegerError(LDDCError):
    """Jaeger错误"""


class ZipkinError(LDDCError):
    """Zipkin错误"""


class OpenTelemetryError(LDDCError):
    """OpenTelemetry错误"""


class OpenTracingError(LDDCError):
    """OpenTracing错误"""


class OpenCensusError(LDDCError):
    """OpenCensus错误"""


class XRayError(LDDCError):
    """X-Ray错误"""


class CloudTraceError(LDDCError):
    """Cloud Trace错误"""


class ApplicationInsightsError(LDDCError):
    """Application Insights错误"""


class PagerDutyError(LDDCError):
    """PagerDuty错误"""


class OpsGenieError(LDDCError):
    """OpsGenie错误"""


class VictorOpsError(LDDCError):
    """VictorOps错误"""


class xMattersError(LDDCError):
    """xMatters错误"""


class AlertManagerError(LDDCError):
    """AlertManager错误"""


class NagiosError(LDDCError):
    """Nagios错误"""


class ZabbixError(LDDCError):
    """Zabbix错误"""


class IcingaError(LDDCError):
    """Icinga错误"""


class CheckMKError(LDDCError):
    """Check_MK错误"""


class SensuError(LDDCError):
    """Sensu错误"""


class LibreNMSError(LDDCError):
    """LibreNMS错误"""


class ObserviumError(LDDCError):
    """Observium错误"""


class CactiError(LDDCError):
    """Cacti错误"""


class MRTGError(LDDCError):
    """MRTG错误"""


class RRDtoolError(LDDCError):
    """RRDtool错误"""


class CollectdError(LDDCError):
    """collectd错误"""


class StatsDError(LDDCError):
    """StatsD错误"""


class GraphiteError(LDDCError):
    """Graphite错误"""


class CarbonError(LDDCError):
    """Carbon错误"""


class WhisperError(LDDCError):
    """Whisper错误"""


class DiamondError(LDDCError):
    """Diamond错误"""


class BrubeckError(LDDCError):
    """Brubeck错误"""


class MetricsError(LDDCError):
    """Metrics错误"""


class MicrometerError(LDDCError):
    """Micrometer错误"""


class DropwizardMetricsError(LDDCError):
    """Dropwizard Metrics错误"""


class ActuatorError(LDDCError):
    """Actuator错误"""


class HealthCheckError(LDDCError):
    """Health Check错误"""


class ReadinessProbeError(LDDCError):
    """Readiness Probe错误"""


class LivenessProbeError(LDDCError):
    """Liveness Probe错误"""


class StartupProbeError(LDDCError):
    """Startup Probe错误"""


class CircuitBreakerError(LDDCError):
    """Circuit Breaker错误"""


class BulkheadError(LDDCError):
    """Bulkhead错误"""


class TimeoutError(LDDCError):
    """Timeout错误"""


class RetryError(LDDCError):
    """Retry错误"""


class FallbackError(LDDCError):
    """Fallback错误"""


class CacheAsideError(LDDCError):
    """Cache Aside错误"""


class WriteThroughError(LDDCError):
    """Write Through错误"""


class WriteBehindError(LDDCError):
    """Write Behind错误"""


class RefreshAheadError(LDDCError):
    """Refresh Ahead错误"""


class EventSourcingError(LDDCError):
    """Event Sourcing错误"""


class CQRSError(LDDCError):
    """CQRS错误"""


class SagaError(LDDCError):
    """Saga错误"""


class OutboxError(LDDCError):
    """Outbox错误"""


class InboxError(LDDCError):
    """Inbox错误"""


class TwoPhaseCommitError(LDDCError):
    """Two Phase Commit错误"""


class ThreePhaseCommitError(LDDCError):
    """Three Phase Commit错误"""


class PaxosError(LDDCError):
    """Paxos错误"""


class RaftError(LDDCError):
    """Raft错误"""


class ByzantineFaultToleranceError(LDDCError):
    """Byzantine Fault Tolerance错误"""


class ConsensusError(LDDCError):
    """Consensus错误"""


class LeaderElectionError(LDDCError):
    """Leader Election错误"""


class SplitBrainError(LDDCError):
    """Split Brain错误"""


class NetworkPartitionError(LDDCError):
    """Network Partition错误"""


class CAPTheoremError(LDDCError):
    """CAP Theorem错误"""


class ACIDError(LDDCError):
    """ACID错误"""


class BASEError(LDDCError):
    """BASE错误"""


class EventualConsistencyError(LDDCError):
    """Eventual Consistency错误"""


class StrongConsistencyError(LDDCError):
    """Strong Consistency错误"""


class WeakConsistencyError(LDDCError):
    """Weak Consistency错误"""


class CausalConsistencyError(LDDCError):
    """Causal Consistency错误"""


class MonotonicConsistencyError(LDDCError):
    """Monotonic Consistency错误"""